from django.core.exceptions import ValidationError
from quiz.models.question_model import Question
from quiz.models.answer_model import Answer
from account.models.instructor_model import InstructorProfile
from school.models.class_model import Class
from school.models.student_list_model import StudentList
from account.models.parent_profile_model import ParentProfile
from account.models.child_list_model import ChildList
from rest_framework import serializers
from quiz.models.taking_quiz_model import TakingQuiz
from rest_framework.serializers import ModelSerializer
from quiz.models import TakingQuizAnswer
from account.models import ChildProfile
from quiz.models import Quiz
from rest_framework import status

class TakingQuizAnswersSerializer(ModelSerializer):
    """
        This is a helper serializer. Cannot be use anywhere else.
    """
    class Meta:
        model = TakingQuizAnswer
        exclude = ["created_at", "updated_at"]


class TakingQuizSerializer(ModelSerializer):
    answers = TakingQuizAnswersSerializer(many=True, source="taking_quizes")

    class Meta:
        model = TakingQuiz
        fields = "__all__"


class ChildSerializer(ModelSerializer):
    """
        This is a helper serializer. Cannot be use anywhere else.
    """
    quiz_history = TakingQuizSerializer(source="child_taking_quiz", many=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    gender = serializers.CharField(source="user.get_gender_display")
    user_type = serializers.CharField(source="user.get_user_type_display")

    class Meta:
        model = ChildProfile
        fields = "__all__"


class ChildListSerializer(ModelSerializer):
    """
        This is a helper serializer. Cannot be use anywhere else.
    """
    child = ChildSerializer()

    class Meta:
        model = ChildList
        exclude = ["parent"]


class TakingQuizDetailsForParentSerializer(ModelSerializer):
    """
        Serializer for list of parent's children. This list has quiz results.
    """
    children = ChildListSerializer(many=True, source="parent_children")

    class Meta:
        model = ParentProfile
        fields = "__all__"


class StudentListSerializer(ModelSerializer):
    """
        This is a helper serializer. Cannot be use anywhere else.
    """
    student = ChildSerializer(source="child")

    class Meta:
        model = StudentList
        fields = "__all__"


class ClassSerializer(ModelSerializer):
    """
        This is a helper serializer. Cannot be use anywhere else.
    """
    students = StudentListSerializer(many=True, source="student_list_class")

    class Meta:
        model = Class
        fields = "__all__"


class TakingQuizDetailsForInstructorSerializer(ModelSerializer):
    """
        Serializer for list of instructor's classes. This list has students and students' quiz results.
    """
    classes = ClassSerializer(many=True, source="instructors_school")

    class Meta:
        model = InstructorProfile
        fields = "__all__"


class TakingQuizDetailsForSpecificClassSerializer(ModelSerializer):
    """
        This is a helper serializer. Cannot be use anywhere else.
    """
    students = StudentListSerializer(many=True,
                                     source="student_list_class")
    instructor_first_name = serializers.CharField(
        source="instructor.user.first_name")
    instructor_last_name = serializers.CharField(
        source="instructor.user.last_name")
    instructor_email = serializers.CharField(source="instructor.user.email")
    instructor_gender = serializers.CharField(
        source="instructor.user.get_gender_display")
    instructor_user_type = serializers.CharField(
        source="instructor.user.get_user_type_display")

    class Meta:
        model = Class
        fields = "__all__"


class TakingQuizCreateSerializer(ModelSerializer):
    """
        Taking Quiz Create serializer. This serializer is using for create operaitons.
        The model has Child field, but Child field value will fill automatically from the request data.
    """
    class Meta:
        model = TakingQuiz
        exclude = ["child"]


class TakingQuizAnswerCreateSerializer(ModelSerializer):
    """
        Taking Quiz Answer Create serializer. This serializer is using for create operaitons.
    """
    class Meta:
        model = TakingQuizAnswer
        fields = "__all__"

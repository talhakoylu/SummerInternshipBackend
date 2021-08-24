from quiz.models.taking_quiz_answer_model import TakingQuizAnswer
from quiz.models.taking_quiz_model import TakingQuiz
from rest_framework import serializers
from school.models.school_model import School
from school.models.student_list_model import StudentList
from rest_framework.serializers import ModelSerializer
from school.models.class_model import Class
from django.contrib.auth import get_user_model

User = get_user_model()

class TakingQuizAnswerSerializerReport(ModelSerializer):
    class Meta:
        model = TakingQuizAnswer
        exclude = ["taking_quiz_title"]


class QuizHistorySerializerReport(ModelSerializer):
    quiz_title = serializers.CharField(source = "quiz.title")
    quiz_book_name = serializers.CharField(source = "quiz.book.name")
    answers = TakingQuizAnswerSerializerReport(many = True, source = "taking_quizes")
    class Meta:
        model = TakingQuiz
        exclude = ["child"]


class ChildSerializerReport(ModelSerializer):
    hobbies = serializers.CharField(source = "user_child.hobbies")
    quiz_history = QuizHistorySerializerReport(many = True, source = "user_child.child_taking_quiz")
    class Meta:
        model = User
        exclude = [
            "password", "last_login", "identity_number", "is_superuser",
            "is_active", "is_staff", "user_permissions", "groups",
            "date_joined", "user_type"
        ]

class StudenListSerializerReport(ModelSerializer):
    student = ChildSerializerReport(source = "child.user")
    class Meta:
        model = StudentList
        exclude = ["created_at", "updated_at", "child"]


class InstructorSerializerReport(ModelSerializer):
    branch = serializers.CharField(source="user_instructor.branch")
    is_principal = serializers.BooleanField(source = "user_instructor.principal")
    gender_display = serializers.CharField(source="get_gender_display")

    class Meta:
        model = User
        exclude = [
            "password", "last_login", "identity_number", "is_superuser",
            "is_active", "is_staff", "user_permissions", "groups",
            "date_joined", "user_type"
        ]


class ClassSerializerReport(ModelSerializer):
    instructor = InstructorSerializerReport(source="instructor.user")
    students = StudenListSerializerReport(many = True, source = "student_list_class")
    class Meta:
        model = Class
        exclude = [
            "created_at",
            "updated_at",
            "school",
        ]
        


class SchoolSerializerReport(ModelSerializer):
    classes = ClassSerializerReport(many=True, source="classes_school")
    name = serializers.CharField()
    address = serializers.CharField()
    website = serializers.CharField()
    city = serializers.CharField()
    district = serializers.CharField(source="city.district")
    country = serializers.CharField(source="city.country")

    class Meta:
        model = School
        exclude = ["created_at", "updated_at"]
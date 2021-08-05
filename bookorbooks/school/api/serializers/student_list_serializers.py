from school.models.class_model import Class
from account.models.child_profile_model import ChildProfile
from rest_framework.serializers import ModelSerializer
from school.models import StudentList, school_model
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
User = get_user_model()

class UserSerializer(ModelSerializer):
    user_type = serializers.CharField(source="get_user_type_display",
                                      read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "first_name", "last_name", "get_full_name",
            "user_type", "email", "identity_number"
        ]


class ChildSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ChildProfile
        fields = "__all__"


class ClassSerializer(ModelSerializer):
    instructor = serializers.CharField(read_only = True)
    school = serializers.CharField(read_only = True)
    class Meta:
        model = Class
        fields = ["id", "name", "grade", "instructor", "school"]


class StudentListSerializer(ModelSerializer):
    child = ChildSerializer(read_only = True)
    school_class = ClassSerializer(read_only = True)
    class Meta:
        model = StudentList
        fields = "__all__"

class ChildrenForDetailSerailizer(ModelSerializer):
    child = ChildSerializer()

    class Meta:
        model = StudentList
        fields = ["id", "child"]

class StudentListByClassSerializer(ModelSerializer):
    students = ChildrenForDetailSerailizer(many = True, read_only = True, source = "student_list_class")
    class Meta:
        model = Class
        fields = "__all__"


class CreateStudentListItemSerializer(ModelSerializer):
    class Meta:
        model = StudentList
        fields = "__all__"

    def create(self, validated_data):
        """
            If the user wants to add the same student to a class for the second time, it will throw an error.
        """
        instance, created = self.Meta.model.objects.get_or_create(**validated_data)
        if not created:
            raise ValidationError({'error':'Student alreaady added into this class..'})
        return instance


class StudentDestroySerializer(ModelSerializer):
    class Meta:
        model = StudentList
        fields = "__all__"
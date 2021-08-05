from school.models.school_model import School
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from school.models.class_model import Class
from account.models.instructor_model import InstructorProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class SchoolSeriliazer(ModelSerializer):
    class Meta:
        model = School
        fields = ["id", "name", "address", "website"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "identity_number", "email", "get_gender_display", "get_user_type_display"]

class InstructorSerializer(ModelSerializer):
    user = UserSerializer(read_only = True, many = False)
    class Meta:
        model = InstructorProfile
        fields = ["user", "branch"]


class ClassCreateSerializer(ModelSerializer):
    school = serializers.CharField(read_only=True)
    instructor = serializers.CharField(read_only=True)

    class Meta:
        model = Class
        fields = "__all__"

class ClassSerializer(ModelSerializer):
    school = SchoolSeriliazer()
    instructor = InstructorSerializer()

    class Meta:
        model = Class
        fields = "__all__"
from school.models.class_model import Class
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from country.models import City, Country
from rest_framework.serializers import ModelSerializer
from school.models.school_model import School
from account.models import InstructorProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(ModelSerializer):
    gender = serializers.CharField(source="get_gender_display")

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "gender"]


class CountryForCitySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "code"]


class CityForSchoolSerializer(ModelSerializer):
    country = CountryForCitySerializer()

    class Meta:
        model = City
        fields = ["id", "name", "code", "country"]


class SchoolListSerializer(ModelSerializer):
    city = CityForSchoolSerializer()

    class Meta:
        model = School
        fields = "__all__"


class InstructorForClassSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = InstructorProfile
        fields = ["user", "branch"]


class ClassListForSchoolDetailSerializer(ModelSerializer):
    instructor = InstructorForClassSerializer()

    class Meta:
        model = Class
        fields = ["id", "name", "grade", "instructor"]


class SchoolDetailSerializer(ModelSerializer):
    city = CityForSchoolSerializer()
    classes = ClassListForSchoolDetailSerializer(many=True,
                                                 source="classes_school")

    class Meta:
        model = School
        fields = "__all__"
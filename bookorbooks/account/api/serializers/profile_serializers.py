from django.core.validators import validate_email
from constants.account_strings import AccountStrings
from country.models.city_model import City
from account.models.instructor_model import InstructorProfile
from rest_framework import serializers
from account.models.custom_user_model import CustomUser
from rest_framework.serializers import ModelSerializer
from account.models import ChildProfile, ParentProfile
from django.contrib.auth import get_user_model
from school.models import School

User = get_user_model()

def gender_validation(value):
        if value < 1 or value > 3:
            raise serializers.ValidationError(
                AccountStrings.RegisterSerializerStrings.gender_error)

def identity_number_validation(value):
    if (not value.isdecimal()) or len(value) > 11:
        raise serializers.ValidationError(
                AccountStrings.RegisterSerializerStrings.identity_number_error)

class ChildProfileSerializer(ModelSerializer):
    district = serializers.CharField(source = "city.district", read_only = True)
    class Meta:
        model = ChildProfile
        fields = ["city", "hobbies", "district"]


class ParentProfileSerializer(ModelSerializer):
    district = serializers.CharField(source = "city.district", read_only = True)

    class Meta:
        model = ParentProfile
        fields = ["city", "district", "profession"]


class SchoolForInstructorSerializer(ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"


class InstructorProfileSerializer(ModelSerializer):
    class Meta:
        model = InstructorProfile
        fields = ["branch", "school"]


class UserChildProfileSerializer(ModelSerializer):
    user_child = ChildProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id", "first_name", "last_name", "email", "identity_number",
            "gender", "birth_date", "user_child"
        ]

    def validate(self, attrs):
        """
        This method will check if the fields are valid.
        """
        validate_email(attrs["email"])
        gender_validation(attrs["gender"])
        identity_number_validation(attrs["identity_number"])
        return attrs

    def update(self, instance, validated_data):
        """
            Parsing the partial data to save the other table.
        """
        if 'user_child' in validated_data:
            nested_serializer = self.fields['user_child']
            nested_instance = instance.user_child
            nested_data = validated_data.pop('user_child')
            nested_serializer.update(nested_instance, nested_data)
        return super(UserChildProfileSerializer,
                     self).update(instance, validated_data)


class UserParentProfileSerializer(ModelSerializer):
    user_parent = ParentProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id", "first_name", "last_name", "email", "identity_number",
            "gender", "birth_date", "user_parent"
        ]

    def validate(self, attrs):
        """
        This method will check if the fields are valid.
        """
        validate_email(attrs["email"])
        gender_validation(attrs["gender"])
        identity_number_validation(attrs["identity_number"])
        return attrs

    def update(self, instance, validated_data):
        """
            Parsing the partial data to save the other table.
        """
        if 'user_parent' in validated_data:
            nested_serializer = self.fields['user_parent']
            nested_instance = instance.user_parent
            nested_data = validated_data.pop('user_parent')
            nested_serializer.update(nested_instance, nested_data)
        return super(UserParentProfileSerializer,
                     self).update(instance, validated_data)


class UserInstructorProfileSerializer(ModelSerializer):
    user_instructor = InstructorProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id", "first_name", "last_name", "email", "identity_number",
            "gender", "birth_date", "user_instructor"
        ]

    def validate(self, attrs):
        """
        This method will check if the fields are valid.
        """
        validate_email(attrs["email"])
        gender_validation(attrs["gender"])
        identity_number_validation(attrs["identity_number"])
        return attrs

    def update(self, instance, validated_data):
        """
            Parsing the partial data to save the other table.
        """
        if 'user_instructor' in validated_data:
            nested_serializer = self.fields['user_instructor']
            nested_instance = instance.user_instructor
            nested_data = validated_data.pop('user_instructor')
            nested_serializer.update(nested_instance, nested_data)
        return super(UserInstructorProfileSerializer,
                     self).update(instance, validated_data)

class MeSerializer(ModelSerializer):
    """
        A serializer to use on the frontend. This serializer is using user model data for retrieving purpose.
    """
    user_type_value = serializers.CharField(source = "get_user_type_display")
    is_principal = serializers.BooleanField(source="user_instructor.principal")
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "user_type", "user_type_value", "birth_date", "identity_number", "gender", "is_principal"]
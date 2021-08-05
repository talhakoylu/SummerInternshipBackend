from account.models.instructor_model import InstructorProfile
from rest_framework import serializers
from account.models.custom_user_model import CustomUser
from rest_framework.serializers import ModelSerializer
from account.models import ChildProfile, ParentProfile
from django.contrib.auth import get_user_model
from school.models import School

User = get_user_model()


class ChildProfileSerializer(ModelSerializer):
    class Meta:
        model = ChildProfile
        fields = ["city", "hobbies"]


class ParentProfileSerializer(ModelSerializer):
    class Meta:
        model = ParentProfile
        fields = ["city", "profession"]


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

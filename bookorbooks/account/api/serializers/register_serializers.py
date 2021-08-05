from rest_framework.utils import field_mapping
from constants.account_strings import AccountStrings
from django.core.validators import validate_email
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from account.models import ChildProfile
from country.models import City

User = get_user_model()


class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id", "email", "username", "password", "first_name", "last_name",
            "identity_number", "user_type", "gender", "birth_date"
        ]

    def user_type_validation(self, value):
        if value < 1 or value > 4:
            raise serializers.ValidationError(
                AccountStrings.RegisterSerializerStrings.user_type_error)

    def gender_validation(self, value):
        if value < 1 or value > 3:
            raise serializers.ValidationError(
                AccountStrings.RegisterSerializerStrings.gender_error)

    def identity_number_validation(self, value):
        if not value.isdecimal() or len(value) != 11:
            raise serializers.ValidationError(
                AccountStrings.RegisterSerializerStrings.identity_number_error)

    def validate(self, attrs):
        """
        This method will check if the fields are valid.
        """
        validate_password(attrs["password"])
        validate_email(attrs["email"])
        self.user_type_validation(attrs["user_type"])
        self.gender_validation(attrs["gender"])
        self.identity_number_validation(attrs["identity_number"])
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            identity_number=validated_data["identity_number"],
            user_type=validated_data["user_type"],
            gender=validated_data["gender"],
            birth_date=validated_data["birth_date"],
        )

        return user


class ChangePasswordSerializer(Serializer):
    model = User
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)

    def validate_new_password(self, value):
        """
            Validation process of the new password field.
        """
        validate_password(value)
        return value
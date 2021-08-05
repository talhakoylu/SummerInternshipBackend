from account.models.child_profile_model import ChildProfile
from book.models.reading_history_model import ReadingHistory
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from book.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()

class BookSerializer(ModelSerializer):
    author = serializers.CharField()
    language = serializers.CharField()
    category = serializers.CharField()
    level = serializers.CharField()
    class Meta:
        model = Book
        fields = "__all__"

class ReadingHistorySerializer(ModelSerializer):
    book = BookSerializer()
    child_name = serializers.CharField(source = "child")
    child_id = serializers.IntegerField(source = "child.user_id")
    class Meta:
        model = ReadingHistory
        exclude = ["child"]

class ReadingHistoryForByChildSerializer(ModelSerializer):
    book = BookSerializer()
    class Meta:
        model = ReadingHistory
        exclude = ["child"]

class UserSerializer(ModelSerializer):
    gender = serializers.CharField(source = "get_gender_display")
    user_type = serializers.CharField(source = "get_user_type_display")
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "gender", "user_type"]

class ChildReadingHistorySerializer(ModelSerializer):
    first_name = serializers.CharField(source = "user.first_name")
    last_name = serializers.CharField(source = "user.last_name")
    email = serializers.CharField(source = "user.email")
    gender = serializers.CharField(source = "user.get_gender_display")
    user_type = serializers.CharField(source = "user.get_user_type_display")
    books = ReadingHistoryForByChildSerializer(many = True, source = "child_reading_history")
    class Meta:
        model = ChildProfile
        fields = ["user", "first_name", "last_name", "email", "gender", "user_type", "city", "hobbies", "books"]


class ReadingHistoryCreateSerializer(ModelSerializer):
    class Meta:
        model = ReadingHistory
        exclude = ["child"]

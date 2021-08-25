from account.models.child_profile_model import ChildProfile
from school.models.school_model import School
from django.db.models.aggregates import Avg, Count, Sum
from school.models.class_model import Class
from school.models.student_list_model import StudentList
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from book.models import ReadingHistory, Book

User = get_user_model()

class BookForReadingHistorySerializer(ModelSerializer):
    category = serializers.CharField()
    category_english = serializers.CharField(source = "category.title_english")
    level = serializers.CharField()
    level_english = serializers.CharField(source = "level.title_english")
    language = serializers.CharField()
    author = serializers.CharField()
    class Meta:
        model = Book
        exclude = ["description", "created_at", "updated_at", "page"]

class ChildReadingHistorySerializer(ModelSerializer):
    book = BookForReadingHistorySerializer()
    class Meta:
        model = ReadingHistory
        exclude = ["child"]


class ChildWithReadingHistorySerializer(ModelSerializer):
    hobbies = serializers.CharField(source="user_child.hobbies")
    reading_history = ChildReadingHistorySerializer(
        many=True, source="user_child.child_reading_history")

    class Meta:
        model = User
        exclude = [
            "password", "last_login", "identity_number", "is_superuser",
            "is_active", "is_staff", "user_permissions", "groups",
            "date_joined", "user_type"
        ]

class StudenListReadingHistoryReportSerializer(ModelSerializer):
    student = ChildWithReadingHistorySerializer(source="child.user")

    class Meta:
        model = StudentList
        exclude = ["created_at", "updated_at", "child"]


class InstructorForClassSerializer(ModelSerializer):
    branch = serializers.CharField(source="user_instructor.branch")
    is_principal = serializers.BooleanField(source="user_instructor.principal")
    gender_display = serializers.CharField(source="get_gender_display")

    class Meta:
        model = User
        exclude = [
            "password", "last_login", "identity_number", "is_superuser",
            "is_active", "is_staff", "user_permissions", "groups",
            "date_joined", "user_type"
        ]


class ClassReadingHistoryReportSerializer(ModelSerializer):
    instructor = InstructorForClassSerializer(source="instructor.user")
    students = StudenListReadingHistoryReportSerializer(many=True,
                                          source="student_list_class")
    avg_read_book = serializers.SerializerMethodField()
    total_read_of_class = serializers.SerializerMethodField()

    class Meta:
        model = Class
        exclude = [
            "created_at",
            "updated_at",
            "school",
        ]

    def get_avg_read_book(self, obj):
        data = Class.objects.filter(id = obj.id).aggregate(sum_read=Sum('student_list_class__child__child_reading_history__counter'), count_child=Count('student_list_class__child__child_reading_history__child', distinct=True))
        if (data["sum_read"] == None) or (data["count_child"] == 0) or (data["sum_read"] == 0) or (data["count_child"] == None):
            return 0
        result = data["sum_read"] / data["count_child"]
        return result
    
    def get_total_read_of_class(self, obj):
        sum_read_book = Class.objects.filter(id = obj.id).aggregate(sum_read=Sum('student_list_class__child__child_reading_history__counter'))
        if (sum_read_book["sum_read"] == None) or (sum_read_book["sum_read"] == 0):
            return 0
        return sum_read_book["sum_read"]

class SchoolReadingHistoryReportSerializer(ModelSerializer):
    classes = ClassReadingHistoryReportSerializer(many=True, source="classes_school")
    name = serializers.CharField()
    address = serializers.CharField()
    website = serializers.CharField()
    city = serializers.CharField()
    district = serializers.CharField(source="city.district")
    country = serializers.CharField(source="city.country")

    class Meta:
        model = School
        exclude = ["created_at", "updated_at"]
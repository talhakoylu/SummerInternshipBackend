from school.models.student_list_model import StudentList
from school.models.class_model import Class
from school.models.school_model import School
from django.contrib import admin

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "website", "address"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "website", "address"]
    class Meta:
        model = School


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "grade", "instructor", "school"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "instructor__user__first_name", "school__name"]
    autocomplete_fields = ["school"]
    class Meta:
        model = Class


@admin.register(StudentList)
class StudentListAdmin(admin.ModelAdmin):
    list_display = ["id", "child", "school_class"]
    list_display_links = ["id", "child"]
    search_fields = ["child", "school_class"]
    autocomplete_fields = ["school_class"]
    class Meta:
        model = StudentList
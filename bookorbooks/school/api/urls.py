from school.api.views.student_list_views import AddStudentListItemAPIView, StudentListAPIView, StudentListByClassAPIView, StudentListDestroyAPIView
from school.api.views.class_views import ClassListAPIView, CreateClassAPIView, UpdateDestroyClassAPIView
from school.api.views.school_views import SchoolDetailAPIView, SchoolListAPIView
from django.urls import path

app_name = "school"

urlpatterns = [
    path("school-list", SchoolListAPIView.as_view(), name="school_list"),
    path("school-detail/<id>",
         SchoolDetailAPIView.as_view(),
         name="school_detail"),
    path("class-list", ClassListAPIView.as_view(), name="list_class"),
    path("class-add", CreateClassAPIView.as_view(), name="add_class"),
    path("class-update/<id>",
         UpdateDestroyClassAPIView.as_view(),
         name="update_class"),
    path("add-student-list-item", AddStudentListItemAPIView.as_view(), name= "add_student_list_item"),
    path("student-list", StudentListAPIView.as_view(), name= "student_list"),
    path("student-list-by-class-instructor", StudentListByClassAPIView.as_view(), name= "student_list_by_class_instructor"),
    path("student-list-item-destroy/<class_id>-<child_id>", StudentListDestroyAPIView.as_view(), name= "student_list_item_destroy"),
]

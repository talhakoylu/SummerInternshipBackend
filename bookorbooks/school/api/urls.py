from school.api.views.school_quiz_history_views import GetAllClassesBySchoolPrincipalAPIView, GetAllSchoolClassStudentByCountryAPIView, GetClassStudentQuizHistoryByInstructor
from school.api.views.school_reading_history_views import GetAllClassReadingHistoryByPrincipalAPIView, GetAllSchoolClassStudentReadingHistoryByCountryAPIView, GetClassStudentReadingHistoryByInstructor
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

    path("reports/get-all-class-reading-history-by-principal", GetAllClassReadingHistoryByPrincipalAPIView.as_view(), name= "get_all_class_reading_history_principal"),
    path("reports/get-all-class-reading-history-by-country-for-principal", GetAllSchoolClassStudentReadingHistoryByCountryAPIView.as_view(), name= "get_all_class_reading_history_country_for_principal"),
    path("reports/get-class-reading-history-by-instructor", GetClassStudentReadingHistoryByInstructor.as_view(), name= "get_class_reading_history_instructor"),

    path("reports/get-all-classes-quiz-history-by-school-principal", GetAllClassesBySchoolPrincipalAPIView.as_view(), name="get_all_classes_quiz_history_by_school_principal"),
    path("reports/get-all-class-quiz-history-by-country-for-principal", GetAllSchoolClassStudentByCountryAPIView.as_view(), name="get_all_class_quiz_history_country_for_principal"),
     path("reports/get-class-quiz-history-by-instructor", GetClassStudentQuizHistoryByInstructor.as_view(), name= "get_class_quiz_history_instructor"),

]

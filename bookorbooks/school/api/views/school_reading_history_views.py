from school.models.class_model import Class
from django.shortcuts import get_object_or_404
from account.api.permissions import IsInstructor, IsPrincipalInstructor
from rest_framework.permissions import IsAuthenticated
from school.api.serializers.school_reading_history_report_serializers import ClassReadingHistoryReportSerializer, SchoolReadingHistoryReportSerializer
from school.models.school_model import School
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.contrib.auth import get_user_model
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter

User = get_user_model()

class GetAllClassReadingHistoryByPrincipalAPIView(RetrieveAPIView):
    """
    Returns the reading history, average number of books read, and total number of books read for all classes in the school. Only School Principal level people can see the data.
    """
    queryset = School.objects.all()
    serializer_class = SchoolReadingHistoryReportSerializer
    permission_classes = [IsAuthenticated, IsInstructor, IsPrincipalInstructor]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(School, id=self.request.user.user_instructor.school.id)
        self.check_object_permissions(self.request, obj)
        return obj

class GetAllSchoolClassStudentReadingHistoryByCountryAPIView(ListAPIView):
    """
    Returns data for all schools. You can access reading data of other schools by searching with values such as school name, country name or using filters. Only School Principal level people can see the data.
    """
    queryset = School.objects.all()
    serializer_class = SchoolReadingHistoryReportSerializer
    permission_classes = [IsAuthenticated, IsInstructor, IsPrincipalInstructor]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['city__country__name', 'city__country__code', 'city__name', 'city__district__name', 'name']
    filterset_fields = ['city__country', 'city__district', 'city']


class GetClassStudentReadingHistoryByInstructor(ListAPIView):
    """
    Returns a list of the classes the instructor is in and the reading histories of the students in those classes.
    """
    queryset = School.objects.all()
    serializer_class = ClassReadingHistoryReportSerializer
    permission_classes = [IsAuthenticated, IsInstructor]
    
    def get_queryset(self):
        return Class.objects.filter(instructor = self.request.user.user_instructor)
    
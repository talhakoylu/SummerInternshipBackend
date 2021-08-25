from school.models.class_model import Class
from school.api.serializers.school_quiz_history_report_serializers import ClassSerializerReport, SchoolSerializerReport
from django.shortcuts import get_object_or_404
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from school.models.school_model import School
from account.api.permissions import IsInstructor, IsPrincipalInstructor
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView

class GetAllClassesBySchoolPrincipalAPIView(RetrieveAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializerReport
    permission_classes = [IsAuthenticated, IsInstructor, IsPrincipalInstructor]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(School, id=self.request.user.user_instructor.school.id)
        self.check_object_permissions(self.request, obj)
        return obj


class GetAllSchoolClassStudentByCountryAPIView(ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializerReport
    permission_classes = [IsAuthenticated, IsInstructor, IsPrincipalInstructor]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['city__country__name', 'city__country__code', 'city__name', 'city__district__name', 'name']
    filterset_fields = ['city__country', 'city__district', 'city']


class GetClassStudentQuizHistoryByInstructor(ListAPIView):
    """
    Returns a list of the classes the instructor is in and the quiz histories of the students in those classes.
    """
    queryset = School.objects.all()
    serializer_class = ClassSerializerReport
    permission_classes = [IsAuthenticated, IsInstructor]
    
    def get_queryset(self):
        return Class.objects.filter(instructor = self.request.user.user_instructor)
    
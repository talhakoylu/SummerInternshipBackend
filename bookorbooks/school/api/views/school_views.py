from school.api.serializers.school_serializers import SchoolDetailSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from school.models.school_model import School
from school.api.serializers import SchoolListSerializer


class SchoolListAPIView(ListAPIView):
    """
        Returns a list of all schools.
    """
    queryset = School.objects.all()
    serializer_class = SchoolListSerializer

class SchoolDetailAPIView(RetrieveAPIView):
    """
        Returns a response that including school detail and the list of classes in that school.
    """
    queryset = School.objects.all()
    serializer_class = SchoolDetailSerializer
    lookup_field = "id"
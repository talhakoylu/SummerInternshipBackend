from school.api.serializers.class_serializers import ClassSerializer
from school.api.permissions import IsOwnClass
from account.api.permissions import IsInstructor, IsInstructorHasSchool
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from school.api import serializers
from school.models.class_model import Class
from school.api.serializers import ClassCreateSerializer


class ClassListAPIView(ListAPIView):
    """
        Returns a list of all classes
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class CreateClassAPIView(CreateAPIView):
    """
        Provides an API view that classes can be created.
    """
    queryset = Class.objects.all()
    serializer_class = ClassCreateSerializer
    permission_classes = [IsAuthenticated, IsInstructor, IsInstructorHasSchool]

    def perform_create(self, serializer):
        """
            School and instructor data are automatically included from request details.
        """
        serializer.save(instructor=self.request.user.user_instructor,
                        school=self.request.user.user_instructor.school)


class UpdateDestroyClassAPIView(RetrieveUpdateDestroyAPIView):
    """
        Provides an API view about updating and destroying the Class object. 

        Permissiion Class:
            IsOwnClass -> If the user is an instructor, but at the same time isn't the owner of the record,
            can't change or destroy the data.
    """
    queryset = Class.objects.all()
    serializer_class = ClassCreateSerializer
    permission_classes = [IsAuthenticated, IsInstructor, IsOwnClass]
    lookup_field = "id"

    def perform_update(self, serializer):
        """
            School and instructor data are automatically included from request details.
        """
        serializer.save(instructor=self.request.user.user_instructor,
                        school=self.request.user.user_instructor.school)

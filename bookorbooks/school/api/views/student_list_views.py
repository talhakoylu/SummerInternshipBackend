from school.api.permissions import IsOwnStudent
from school.models.class_model import Class
from rest_framework.permissions import IsAuthenticated
from school.api.serializers.student_list_serializers import CreateStudentListItemSerializer, StudentListByClassSerializer, StudentListSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveDestroyAPIView, get_object_or_404
from school.models.student_list_model import StudentList
from account.api.permissions import IsInstructor
from rest_framework.response import Response


class AddStudentListItemAPIView(CreateAPIView):
    """
        A view used to add data to the Student List.
    """
    queryset = StudentList.objects.all()
    serializer_class = CreateStudentListItemSerializer
    permission_classes = [IsAuthenticated, IsInstructor]

    def create(self, request, *args, **kwargs):
        """
        verify that the POST has the request user as the owner of the class
        """
        result = Class.objects.filter(id = request.data.get("school_class",)).filter(instructor_id = request.user.id)
        if result.count() == 1:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        return Response({"error": "To do this, you must be the instructor of this class."},status = 403)

class StudentListAPIView(ListAPIView):
    """
        Returns a list of all student - class relations.
    """
    queryset = StudentList.objects.all()
    serializer_class = StudentListSerializer


class StudentListByClassAPIView(ListAPIView):
    """
        Returns a list of classes owned by the teacher and students in those classes.
    """
    serializer_class = StudentListByClassSerializer
    permission_classes = [IsAuthenticated, IsInstructor]

    def get_queryset(self):
        return Class.objects.filter(instructor = self.request.user.id)


class StudentListDestroyAPIView(RetrieveDestroyAPIView):
    """
        Returns a destroy view by child id value.
    """
    queryset = StudentList.objects.all()
    serializer_class = StudentListSerializer
    permission_classes = [IsAuthenticated, IsInstructor, IsOwnStudent]
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(StudentList,child = self.kwargs["child_id"], school_class = self.kwargs["class_id"])
        self.check_object_permissions(self.request, obj)
        return obj
from rest_framework.permissions import IsAuthenticated
from account.api.permissions import IsChild, IsInstructor, IsParent
from account.api.serializers.profile_serializers import UserChildProfileSerializer, UserInstructorProfileSerializer, UserParentProfileSerializer
from account.api.serializers.child_list_serializers import User
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import get_user_model

User = get_user_model()


class ChildProfileUpdateAPIView(RetrieveUpdateAPIView):
    """
        Provides a "child profile update" page API.
    """
    queryset = User.objects.all()
    serializer_class = UserChildProfileSerializer
    permission_classes = [IsAuthenticated, IsChild]

    def get_object(self):
        """
            Retrieves user details from the request.
        """
        queryset = self.get_queryset()
        obj = User.objects.get(id=self.request.user.id)
        return obj

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ParentProfileUpdateAPIView(RetrieveUpdateAPIView):
    """
        Provides a "parent profile update" page API.
    """
    queryset = User.objects.all()
    serializer_class = UserParentProfileSerializer
    permission_classes = [IsAuthenticated, IsParent]

    def get_object(self):
        """
            Retrieves user details from the request.
        """
        queryset = self.get_queryset()
        obj = User.objects.get(id=self.request.user.id)
        return obj

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class InstructorProfileUpdateAPIView(RetrieveUpdateAPIView):
    """
        Provides an "instructor profile update" page API.
    """
    queryset = User.objects.all()
    serializer_class = UserInstructorProfileSerializer
    permission_classes = [IsAuthenticated, IsInstructor]

    def get_object(self):
        """
            Retrieves user details from the request.
        """
        queryset = self.get_queryset()
        obj = User.objects.get(id=self.request.user.id)
        return obj

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


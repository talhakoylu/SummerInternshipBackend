from account.models.parent_profile_model import ParentProfile
from account.api.permissions import IsOwnChild, IsParent
from account.api.serializers.child_list_serializers import ChildListByParentSerializer, ChildListSerializer, ChildRecordAddSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, get_object_or_404
from account.models import ChildList
from rest_framework.permissions import IsAuthenticated

class ChildListAPIView(ListAPIView):
    """
        Returns a list of all child - parent relations.
    """
    queryset = ChildList.objects.all()
    serializer_class = ChildListSerializer


class ChildListCreateAPIView(CreateAPIView):
    """
        A parent can add a child as their child.
    """

    queryset = ChildList.objects.all()
    serializer_class = ChildRecordAddSerializer
    permission_classes = [IsAuthenticated, IsParent]

    def perform_create(self, serializer):
        serializer.save(parent=self.request.user.user_parent)


class ChildListByUserAPIView(RetrieveAPIView):
    """
        Returns a list of the parent's children.
    """
    queryset = ParentProfile.objects.all()
    serializer_class = ChildListByParentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(ParentProfile, user=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

class ChildListItemDestroyAPIView(RetrieveDestroyAPIView):
    """
        Returns a destroy view by child id value.
    """
    queryset = ChildList.objects.all()
    serializer_class = ChildListSerializer
    permission_classes = [IsAuthenticated, IsParent, IsOwnChild]
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(ChildList,child = self.kwargs["child_id"])
        self.check_object_permissions(self.request, obj)
        return obj

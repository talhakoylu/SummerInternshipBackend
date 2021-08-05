from book.api.permissions import IsParentOrInstructor
from utils.general_permissions import IsSuperUser
from django.shortcuts import get_list_or_404
from account.api.permissions import IsChild, IsParent
from rest_framework.permissions import IsAuthenticated
from account.models.child_profile_model import ChildProfile
from book.api.serializers.reading_history_serializers import ChildReadingHistorySerializer, ReadingHistoryCreateSerializer, ReadingHistoryForByChildSerializer, ReadingHistorySerializer
from book.models.reading_history_model import ReadingHistory
from rest_framework.generics import CreateAPIView, ListAPIView
from datetime import datetime


class ReadingHistoryListAllAPIView(ListAPIView):
    """
        Returns the list of all read histories.
    """
    queryset = ReadingHistory.objects.all()
    serializer_class = ReadingHistorySerializer
    permission_classes = [IsAuthenticated, IsSuperUser]


class ReadingHistoryByChildAPIView(ListAPIView):
    """
        Returns the list of all read history by current logged in child user.
    """
    serializer_class = ChildReadingHistorySerializer
    permission_classes = [IsAuthenticated, IsChild]

    def get_queryset(self):
        return ChildProfile.objects.filter(user=self.request.user.id)

class ReadingHistoryByChildIdAPIView(ListAPIView):
    """
        Returns the read history according to the Child Id value. To see this page,
        you must be logged in as a parent or an instructor.
    """
    serializer_class = ReadingHistoryForByChildSerializer
    permission_classes = [IsAuthenticated, IsParentOrInstructor]
    
    def get_queryset(self):
        return get_list_or_404(ReadingHistory, child_id = self.kwargs["child_id"])


class AddReadingHistoryAPIView(CreateAPIView):
    """
        Read history record add page. This api need 3 paramters, they are book id, is finished and child id.
        Child id value is getting from the request by currently logged in user. 
    """
    queryset = ReadingHistory.objects.all()
    serializer_class = ReadingHistoryCreateSerializer
    permission_classes = [IsAuthenticated, IsChild]

    def perform_create(self, serializer):
        """
            Normally, a new record is added to the table every time a request is made. If we make an update page, 
            we need to find current object with value. For avoiding this stages we override perform_create method.
            With this method, if a book and a child record has already in same row just works update method of object.
            However, if there is no record about the book and the child, works create method of object. 
        """
        book = serializer.validated_data["book"]
        is_finished = serializer.validated_data.get('is_finished', )
        child = self.request.user.user_child
        obj_lst = ReadingHistory.objects.filter(book=book.pk, child=child)
        counter = obj_lst[0].counter
        if obj_lst:
            if is_finished == False:
                return obj_lst.update(is_finished=is_finished, updated_at=datetime.now())
            counter += 1
            return obj_lst.update(is_finished=is_finished, updated_at=datetime.now(), counter = counter)
        else:
            return ReadingHistory.objects.create(book_id=book.pk,
                                          child=child,
                                          is_finished=is_finished)

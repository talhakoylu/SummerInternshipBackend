from account.api.permissions import IsChild
from rest_framework.permissions import IsAuthenticated
from book.api.serializers import BookPageSerializer
from book.models import BookPage
from rest_framework.generics import ListAPIView


class BooksPageListAPIView(ListAPIView):
    """
    Returns the list of all book pages.
    """
    queryset = BookPage.objects.all()
    serializer_class = BookPageSerializer


class BookPagesByBookIdAPIView(ListAPIView):
    """
    Returns the list of all book pages.
    """
    queryset = BookPage.objects.all()
    serializer_class = BookPageSerializer
    permission_classes = [IsAuthenticated, IsChild]
    lookup_field = "book_id"
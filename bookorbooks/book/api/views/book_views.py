from book.api.serializers import BookSerializer, BookDetailSerializer
from book.models import Book
from rest_framework.generics import ListAPIView, RetrieveAPIView


class BookListAPIView(ListAPIView):
    """
    Returns the list of all books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailAPIView(RetrieveAPIView):
    """
    Returns a specific book with using the slug value of the Book.
    """
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    lookup_field = "slug"
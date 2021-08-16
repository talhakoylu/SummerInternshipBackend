from rest_framework.filters import SearchFilter
from book.api.serializers import BookSerializer, BookDetailSerializer
from book.models import Book
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend


class BookListAPIView(ListAPIView):
    """
    Returns the list of all books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name", "description"]
    filterset_fields = ['category', 'level', 'language']


class BookDetailAPIView(RetrieveAPIView):
    """
    Returns a specific book with using the slug value of the Book.
    """
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    lookup_field = "slug"
    
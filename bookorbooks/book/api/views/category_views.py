from book.api.serializers import CategorySerializer, CategoryDetailWithBooksSerializer
from book.models import Category
from rest_framework.generics import ListAPIView, RetrieveAPIView


class CategoryListAPIView(ListAPIView):
    """Returns the list of categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailAPIView(RetrieveAPIView):
    """
    Returns a specific category with using the slug value of the category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"

class CategoryDetailWithBooksAPIView(RetrieveAPIView):
    """
    Returns a specific category and also returns a list of books that category with using the slug value of the category.
    """
    queryset = Category.objects.all()
    serializer_class = CategoryDetailWithBooksSerializer
    lookup_field = "slug"
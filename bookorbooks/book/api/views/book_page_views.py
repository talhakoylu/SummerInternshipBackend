from book.api.serializers import BookPageSerializer
from book.models import BookPage
from rest_framework.generics import ListAPIView


class BooksPageListAPIView(ListAPIView):
    """
    Returns the list of all book pages.
    """
    queryset = BookPage.objects.all()
    serializer_class = BookPageSerializer

from book.api.serializers import BookLevelSerializer
from book.models import BookLevel
from rest_framework.generics import ListAPIView


class BookLevelListAPIView(ListAPIView):
    """Returns the list of Book Levels"""
    queryset = BookLevel.objects.all()
    serializer_class = BookLevelSerializer
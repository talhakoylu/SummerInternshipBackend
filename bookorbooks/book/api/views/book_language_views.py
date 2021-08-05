from book.api.serializers import BookLanguageSerializer
from book.models import BookLanguage
from rest_framework.generics import ListAPIView


class BookLanguageListAPIView(ListAPIView):
    """Returns the list of Book Languages"""
    queryset = BookLanguage.objects.all()
    serializer_class = BookLanguageSerializer

from book.api.serializers import AuthorSerializer, AuthorDetailSerializer
from book.models import Author
from rest_framework.generics import ListAPIView, RetrieveAPIView


class AuthorListAPIView(ListAPIView):
    """Returns the list of Authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailAPIView(RetrieveAPIView):
    """
    Returns a specific author with using Author's slug value
    """
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer
    lookup_field = "slug"

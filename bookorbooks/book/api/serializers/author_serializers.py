from book.models import Author, Book
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class _BookForAuthorBooksSerializer(serializers.ModelSerializer):
    # helper serializer. It should not be imported elsewhere.
    class Meta:
        model = Book
        fields = ["id", "name", "slug", "cover_image", "page"]


class AuthorDetailSerializer(serializers.ModelSerializer):
    """
    List of author's books included in author's detail data
    """
    books = _BookForAuthorBooksSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = "__all__"

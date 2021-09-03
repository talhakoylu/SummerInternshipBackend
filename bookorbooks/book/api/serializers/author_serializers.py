from book.models import Author, Book
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class _BookForAuthorBooksSerializer(serializers.ModelSerializer):
    # helper serializer. It should not be imported elsewhere.
    category = serializers.CharField()
    category_english = serializers.CharField(source = "category.title_english")
    level = serializers.CharField()
    level_english = serializers.CharField(source = "level.title_english")
    language = serializers.CharField()
    language_code = serializers.CharField(source = "language.language_code")
    class Meta:
        model = Book
        fields = ["id", "name", "slug", "cover_image", "page", "category", "category_english", "level", "level_english", "language", "language_code"]


class AuthorDetailSerializer(serializers.ModelSerializer):
    """
    List of author's books included in author's detail data
    """
    books = _BookForAuthorBooksSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = "__all__"

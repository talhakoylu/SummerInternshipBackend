
from book.models.book_language_model import BookLanguage
from book.models.book_level_model import BookLevel
from book.models.author_model import Author
from rest_framework import serializers
from book.models import Book, BookPage


class BookSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    category_english = serializers.CharField(source = "category.title_english")
    level = serializers.CharField()
    level_english = serializers.CharField(source = "level.title_english")
    author = serializers.CharField()
    language = serializers.CharField()
    language_code = serializers.CharField(source = "language.language_code")
    class Meta:
        model = Book
        fields = "__all__"


class BookPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPage
        fields = "__all__"


class SimpleBookPageSerializer(serializers.ModelSerializer):
    """
    This serializer is making specification on the Book Page JSON Data.\n
    On this way, created_at - updated_at - content fields of Book Page Model are excluding from request result.
    """
    class Meta:
        model = BookPage
        fields = [
            "id", "title", "content", "page_number", "image", "image_position",
            "content_position"
        ]


class AuthorSerializer(serializers.ModelSerializer):
    #helper serializer
    class Meta:
        model = Author
        exclude = ["created_at", "updated_at"]

class BookDetailSerializer(serializers.ModelSerializer):
    """
    List of book's pages included in book's detail data
    """
    book_pages = SimpleBookPageSerializer(many=True, read_only=True)
    category = serializers.CharField()
    category_english = serializers.CharField(source = "category.title_english")
    level = serializers.CharField()
    level_english = serializers.CharField(source = "level.title_english")
    author = AuthorSerializer(many = False)
    language = serializers.CharField()
    language_code = serializers.CharField(source = "language.language_code")
    class Meta:
        model = Book
        fields = "__all__"






from rest_framework import serializers
from book.models import Category, Book, Author, BookLevel, BookLanguage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class _AuthorForCategoryBookSerializer(serializers.ModelSerializer):
    # helper serializer. It should not be imported elsewhere.
    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "full_name"]


class _BookLevelForCategoryBookSerializer(serializers.ModelSerializer):
    # helper serializer. It should not be imported elsewhere.
    class Meta:
        model = BookLevel
        fields = ["id", "title", "title_english"]


class _LanguageForCategoryBookSerializer(serializers.ModelSerializer):
    # helper serializer. It should not be imported elsewhere.
    class Meta:
        model = BookLanguage
        fields = ["id", "language_name", "language_code"]


class _BookForCategorySerializer(serializers.ModelSerializer):
    # helper serializer. It should not be imported elsewhere.
    level = _BookLevelForCategoryBookSerializer(many=False)
    language = _LanguageForCategoryBookSerializer(many=False)
    author = _AuthorForCategoryBookSerializer(many=False)

    class Meta:
        model = Book
        fields = [
            "id", "name", "cover_image", "slug", "author", "level", "language"
        ]


class CategoryDetailWithBooksSerializer(serializers.ModelSerializer):
    books = _BookForCategorySerializer(many=True,
                                      read_only=True,
                                      source="category_books")

    class Meta:
        model = Category
        fields = "__all__"

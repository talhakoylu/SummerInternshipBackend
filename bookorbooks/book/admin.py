from book.models.reading_history_model import ReadingHistory
from django import forms
from book.models import Author, Book, BookLanguage, BookLevel, BookPage, Category
from django.contrib import admin

# Register your models here.


class CategoryAdminForm(forms.ModelForm):
    """
    This class is overrides the description field. In this way, user sees a textfield area
    instead of charfield area.
    """
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={
                'cols': 80,
                'rows': 10
            })
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ["id", "title", "slug", "created_at", "updated_at"]
    list_display_links = ["id", "title"]
    search_fields = ["title"]

    class Meta:
        model = Category


@admin.register(BookLevel)
class BookLevelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at", "updated_at"]
    list_display_links = ["id", "title"]
    search_fields = ["title"]

    class Meta:
        model = BookLevel


@admin.register(BookLanguage)
class BookLanguageAdmin(admin.ModelAdmin):
    list_display = [
        "id", "language_name", "language_code", "created_at", "updated_at"
    ]
    list_display_links = ["id", "language_name", "language_code"]
    search_fields = ["language_name", "language_code"]

    class Meta:
        model = BookLanguage


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        "id", "first_name", "last_name", "slug", "created_at", "updated_at"
    ]
    list_display_links = ["id", "first_name", "last_name"]
    fields = [('first_name', 'last_name'), 'biography', 'photo']

    search_fields = ["first_name", "last_name"]

    class Meta:
        model = Author


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "slug", "page", "author", "level", "language", "category"
    ]
    list_display_links = ["id", "name"]
    fields = [("category", "level"), ("language", "author"), "name",
              "description", "cover_image", "page"]
    search_fields = ["name"]
    autocomplete_fields = ["author", "category", "language", "level"]

    class Meta:
        model = Book


@admin.register(BookPage)
class BookPageAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "page_number", "created_at", "updated_at"]
    list_display_links = ["id", "title"]
    autocomplete_fields = ["book"]

    class Meta:
        model = BookPage


@admin.register(ReadingHistory)
class ReadingHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "__str__", "is_finished", "created_at", "updated_at", "counter"]
    list_display_links = ["id", "__str__"]

    class Meta:
        model = ReadingHistory
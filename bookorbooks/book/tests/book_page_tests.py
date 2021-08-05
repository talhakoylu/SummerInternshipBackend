from django.conf.urls import url
from rest_framework.test import APITestCase
from django.urls import reverse
from book.models import Book, BookPage, Author, Category, BookLevel, BookLanguage


class BookPageTests(APITestCase):
    url = reverse("book:books-page-list")

    def setUp(self) -> None:
        self.author = Author.objects.create(first_name="Ahmet Talha",
                                            last_name="Köylü",
                                            biography="Bio deneme")
        self.category = Category.objects.create(title="Category 1",
                                                description="Açıklama 1")
        self.level = BookLevel.objects.create(title="A")
        self.language = BookLanguage.objects.create(language_name="Türkçe",
                                                    language_code="TUR")
        self.book = Book.objects.create(category=self.category,
                                        language=self.language,
                                        level=self.level,
                                        name="Kitap denemesi",
                                        description="Kitap açıklama denemesi",
                                        author=self.author)
        self.book_page = BookPage.objects.create(book=self.book,
                                                 content="Book page content 1",
                                                 page_number=1)

    def test_get_page_title(self):
        page_title = f"Book: {self.book.name} Page: {self.book_page.page_number}"
        assert page_title == self.book_page.get_page_title

    def test_books_page_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
from django.utils.text import slugify
from rest_framework.test import APITestCase
from django.urls import reverse
import json
from book.models import Book, Author, BookPage, BookLevel, BookLanguage, Category


class BookTests(APITestCase):
    url_list = reverse("book:book-list")

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

    def test_get_slug(self):
        """
        This is an unit test method that checks whether the slug value of the book is created correctly.
        """

        test_slug = slugify(self.book.name.replace("ı", "i"))
        self.assertEqual(test_slug, self.book.slug)

    def test_get_slug_same_name_condition(self):
        """
        This is an unit test method that checks if the second book with the same name wants to be add to the system,
        this test checks that whether the slug value is created correctly. Right situation for this problem is the slug
        value has to be created with a number at the end of the slug value. This number will be increased every add request.
        """

        book2 = Book.objects.create(
            category=self.category,
            language=self.language,
            level=self.level,
            name="Kitap denemesi",
            description=
            "Kitap açıklama denemesi aynı isimli kitap slug testi için",
            author=self.author)
        test_slug = slugify(book2.name.replace("ı", "i")) + "-1"
        self.assertEqual(test_slug, book2.slug)

    def test_book_list(self):
        """
        A unit test that checks whether book list view created successfully and whether the response contains the test data.
        """
        response = self.client.get(self.url_list, format="application/json")
        self.assertTrue(response.status_code == 200)
        self.assertEqual(
            json.loads(response.content)[0]["name"], self.book.name)


class BookDetailTests(APITestCase):
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

    def test_book_detail_view(self):
        """
        This is a unit test that works about book detail page created successfully or not and checks that page includes
        correct data or not.
        """
        url = reverse("book:book-detail", kwargs={"slug": self.book.slug})
        response = self.client.get(url)
        assert response.status_code == 200
        assert json.loads(response.content)["slug"] == self.book.slug

    def test_book_pages(self):
        """
        In serializer class, book detail page includes book pages. This unit test method checks that detail result
        includes book pages or not.
        """
        url = reverse("book:book-detail", kwargs={"slug": self.book.slug})
        response = self.client.get(url)
        assert response.status_code == 200
        assert "book_pages" in json.loads(response.content)
        
    def test_book_detail_foreignkey_fields(self):
        url = reverse("book:book-detail", kwargs={"slug": self.book.slug})
        response = self.client.get(url)
        assert response.status_code == 200
        assert "language" in json.loads(response.content)
        assert "level" in json.loads(response.content)
        assert "level" in json.loads(response.content)
        assert "category" in json.loads(response.content)
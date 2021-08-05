import json
from django.utils.text import slugify
from rest_framework.test import APITestCase
from django.urls import reverse
from book.models import Category, Author, BookLevel, BookLanguage, Book


class CategoryTests(APITestCase):
    url_list = reverse("book:category-list")

    def setUp(self) -> None:
        self.category = Category.objects.create(title="Category 1",
                                                description="Description 1")

    def test_get_slug(self):
        """
        A unit test that checks the category model's get slug method is working correctly or not.
        """
        slug = slugify(self.category.title.replace("ı", "i"))
        self.assertEqual(slug, self.category.slug)

    def test_get_list(self):
        """
        A unit test that checks if the category api's list view is working correctly. 
        """
        response = self.client.get(self.url_list)
        self.assertEqual(200, response.status_code)

    def test_category_detail_page(self):
        """
        A unit test method that checks if the category detail page is working correctly and details are coming.
        """
        url_detail = reverse("book:category-detail",
                             kwargs={"slug": self.category.slug})
        response = self.client.get(url_detail)
        self.assertEqual(200, response.status_code)
        self.assertTrue("title" in json.loads(response.content))


class CategoryWithBooksTests(APITestCase):
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

    def test_category_detail_with_books(self):
        """
        A unique test that checks if the category detail page includes books or not.
        """

        url = reverse("book:category-detail-with-books",
                      kwargs={"slug": self.category.slug})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTrue("books" in json.loads(response.content)
                        and len(json.loads(response.content)["books"]) > 0)

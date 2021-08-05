from django.utils.text import slugify
from rest_framework.test import APITestCase
from django.urls import reverse
from book.models import Author, Book, BookLanguage, BookLevel, Category
import json


class AuthorListTests(APITestCase):
    url = reverse("book:author-list")

    def setUp(self):
        self.author = Author.objects.create(first_name="Ahmet Talha",
                                            last_name="Köylü",
                                            biography="Bio deneme")
        self.author2 = Author.objects.create(first_name="Ahmet Talha",
                                             last_name="Köylü",
                                             biography="Bio deneme 2")

    def test_author_full_name(self):
        """
        A unit test method that controls the get_full_name method of the author model.
        """
        author_instance = Author.objects.get(id=self.author.id)
        full_name = f"{self.author.first_name} {self.author.last_name}"

        self.assertEqual(author_instance.get_full_name(), full_name)

    def test_author_slug_unique(self):
        """
        A unit test method that controls the get_slug method of the author model.
        """
        author_instance = Author.objects.get(id=self.author2.id)
        slug = slugify(author_instance.get_full_name().replace("ı", "i"))

        self.assertEqual(author_instance.slug, slug + "-1")


class AuthorDetailTests(APITestCase):
    def setUp(self):
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

    def test_author_get_detail(self):
        """
        A unit test about author's detail page.
        This method checks the author's number of books and the existence of a detail page.
        """

        url = reverse('book:author-detail', kwargs={'slug': self.author.slug})
        response = self.client.get(url)

        self.assertTrue(
            json.loads(response.content)['slug'] == self.author.slug,
            "Slug field doesn't match. The author details may not occured")

        self.assertTrue(
            len(json.loads(response.content)['books']) == Book.objects.filter(
                author=self.author).count(),
            "The number of books written by the author and the number of books listed are not equal."
        )

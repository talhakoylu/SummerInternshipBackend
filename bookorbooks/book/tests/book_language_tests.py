from django.conf.urls import url
from rest_framework.test import APITestCase
from django.urls import reverse
from book.models import BookLanguage


class BookLanguageTests(APITestCase):
    url = reverse("book:book-language-list")

    def setUp(self) -> None:
        self.book_language = BookLanguage.objects.create(
            language_name="Türkçe", language_code="Tur")

    def test_language_list(self):
        """
        This is a unit test. Main purpose of this test is whether the language list of books is listed correctly after the get request.
        """

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Tur")
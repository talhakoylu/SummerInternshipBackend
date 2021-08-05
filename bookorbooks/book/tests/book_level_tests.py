from django.conf.urls import url
from rest_framework.test import APITestCase
from django.urls import reverse
from book.models import BookLevel


class BookLevelTests(APITestCase):
    url = reverse("book:book-level-list")

    def setUp(self) -> None:
        self.book_level = BookLevel.objects.create(title="A")

    def test_level_list(self):
        """
        This is a unit test. Main purpose of this test is whether the level list of books is listed correctly after the get request.
        """

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "A")
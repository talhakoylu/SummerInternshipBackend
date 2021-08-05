from book.models.reading_history_model import ReadingHistory
from book.models.book_model import Book
from book.models.author_model import Author
from book.models.book_language_model import BookLanguage
from book.models.book_level_model import BookLevel
from book.models.category_model import Category
import json
from django.urls.base import reverse
from rest_framework.test import APITestCase
from django.utils.translation import activate
from django.contrib.auth import get_user_model

User = get_user_model()


class ReadingHistoryTests(APITestCase):
    activate("en")
    url = reverse("book:reading_history_list")
    url_child = reverse("book:reading_history_list_by_child")
    url_add = reverse("book:reading_history_add")
    login_url = reverse("token_obtain_pair")

    def setUp(self) -> None:
        #users
        self.password = "test1234"
        self.user_child = User.objects.create_user(username="johndoe", password=self.password, email="johndoe@example.com", identity_number="1", user_type=2)
        self.user_parent = User.objects.create_user(username="davedoe", password=self.password, email="davedoe@example.com", identity_number="2", user_type=3)
        
        #book
        self.category = Category.objects.create(title="Category Title", description="Category description")
        self.book_level = BookLevel.objects.create(title="A")
        self.book_language = BookLanguage.objects.create(language_name="Language Name", language_code="Language Code")
        self.author = Author.objects.create(first_name="Author", last_name="Doe", biography="Example bio")
        self.book = Book.objects.create(level=self.book_level, category=self.category, author=self.author, language=self.book_language, name="Book Name 1", description="Book description")

        #reading history
        self.reading_history = ReadingHistory.objects.create(book = self.book, child = self.user_child.user_child, is_finished = True, counter = 1)

        self.url_child_id = reverse("book:reading_history_list_by_child_id", kwargs={"child_id" : self.user_child.id})

    def test_jwt_authentication(self, username="johndoe", password="test1234"):
        response = self.client.post(self.login_url, data={"username": username, "password": password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_reading_history_all_is_authenticated(self):
        """
            To see this page, user must be logged in.
        """
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)
    
    def test_reading_history_all_is_superuser(self):
        """
            To see this page, user must be logged in.
        """
        self.test_jwt_authentication()
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)
    
    def test_reading_history_all(self):
        """
            Checks that whether the ReadingHistoryAll page working correctly.
        """
        self.user_child.is_superuser = True
        self.user_child.save()
        self.test_jwt_authentication()
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
    
    def test_reading_history_by_child_is_authenticated(self):
        """
            To see this page, user must be logged in.
        """
        response = self.client.get(self.url_child)
        self.assertEqual(401, response.status_code)
    
    def test_reading_history_by_child_is_child(self):
        """
            To see this page, user must be logged in.
        """
        self.user_child.user_type = 3
        self.user_child.save()
        self.test_jwt_authentication()
        response = self.client.get(self.url_child)
        self.assertEqual(403, response.status_code)

    def test_reading_history_by_child(self):
        """
            ReadingHistoryByChild page returns the result of reading records of current authenticated child user. This unit test checks that whether the ReadingHistoryByChild page working correctly.
        """
        self.test_jwt_authentication()
        response = self.client.get(self.url_child)
        self.assertEqual(200, response.status_code)
    
    def test_reading_history_by_child_id_is_authenticated(self):
        """
            To see this page, user must be logged in.
        """
        response = self.client.get(self.url_child_id)
        self.assertEqual(401, response.status_code)
    
    def test_reading_history_by_child_is_parent_or_instructor(self):
        """
            To see this page, user must be logged in.
        """
        self.test_jwt_authentication()
        response = self.client.get(self.url_child_id)
        self.assertEqual(403, response.status_code)

    def test_reading_history_by_child_id(self):
        """
            ReadingHistoryByChildId page returns the result of reading records of given id value of child user. This unit test checks that whether the ReadingHistoryByChildId page working correctly.
        """
        self.test_jwt_authentication(username = "davedoe")
        response = self.client.get(self.url_child_id)
        self.assertEqual(200, response.status_code)
        self.user_parent.user_type = 4
        self.user_parent.save()
        self.test_jwt_authentication(username = "davedoe")
        response2 = self.client.get(self.url_child_id)
        self.assertEqual(200, response2.status_code)
    
    
    
    def test_reading_history_add_is_authenticated(self):
        """
            To see this page, user must be logged in.
        """
        response = self.client.get(self.url_add)
        self.assertEqual(401, response.status_code)
    
    def test_reading_history_add_is_child(self):
        """
            To see this page, user must be logged in.
        """
        self.test_jwt_authentication(username = "davedoe")
        response = self.client.get(self.url_add)
        self.assertEqual(403, response.status_code)

    def test_reading_history_add(self):
        """
            Checks that if the reading history record add page working correctly.
        """
        self.test_jwt_authentication()
        data = {
            "book": self.book.id,
            "child": self.user_child.id,
            "is_finished": True,
        }
        response = self.client.post(self.url_add, data = data)
        self.assertEqual(201, response.status_code)
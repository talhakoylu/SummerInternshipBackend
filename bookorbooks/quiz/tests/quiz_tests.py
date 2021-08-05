from book.models.author_model import Author
from book.models.book_language_model import BookLanguage
from book.models.book_level_model import BookLevel
from book.models.category_model import Category
from book.models.book_model import Book
import json
from quiz.models.quiz_model import Quiz
from django.utils.translation import activate
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class QuizTests(APITestCase):
    activate('en')
    url = reverse("quiz:quiz_list_all")
    url_enabled = reverse("quiz:enabled_quiz_list_all")
    login_url = reverse("token_obtain_pair")

    def setUp(self) -> None:
        self.username = "johndoe"
        self.password = "test1234"
        self.user = User.objects.create_user(username = self.username, password = self.password)
        self.category = Category.objects.create(title = "Category Title", description = "Category description")
        self.book_level = BookLevel.objects.create(title = "A")
        self.book_language = BookLanguage.objects.create(language_name = "Language Name", language_code = "Language Code")
        self.author = Author.objects.create(first_name = "Author", last_name = "Doe", biography = "Example bio")
        self.book = Book.objects.create(level = self.book_level, category = self.category, author = self.author, language = self.book_language, name = "Book Name 1", description = "Book description")
        self.quiz = Quiz.objects.create(book = self.book, title = "Example Quiz 1", enabled = True)
        self.quiz2 = Quiz.objects.create(book = self.book, title = "Example Quiz 2", enabled = False)

    def test_jwt_authentication(self, username="johndoe", password="test1234"):
        response = self.client.post(self.login_url, data={"username": username, "password": password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_quiz_is_authenticated(self):
        """
            Quiz page cannot show from a guest user. That's why, this test must return 401 status code at the begining, then we called test_jwt_authentication.
            With this way, user would be logged in. After we checked the response2, it must return 200 status code.
        """
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)
        self.test_jwt_authentication()
        response2 = self.client.get(self.url)
        self.assertEqual(200, response2.status_code)

    def test_enabled_quizzes_is_authenticated(self):
        """
            Enabled quiz page cannot show from a guest user. That's why, this test must return 401 status code at the begining, then we called test_jwt_authentication.
            With this way, user would be logged in. After we checked the response2, it must return 200 status code.
        """
        response = self.client.get(self.url_enabled)
        self.assertEqual(401, response.status_code)
        self.test_jwt_authentication()
        response2 = self.client.get(self.url_enabled)
        self.assertEqual(200, response2.status_code)
    
    def test_enabled_quiz_counter(self):
        """
            For the test, there are 2 quizzes were added. The first one is enabled and the second one is disabled.
            We must see only 1 result in this page, because we filtered the results of this page, if the quiz's enabled option is selected by true then show it.
        """
        self.test_jwt_authentication()
        response = self.client.get(self.url_enabled)
        self.assertEqual(200, response.status_code)
        result = json.loads(response.content)
        self.assertTrue(len(result) == 1)
from book.models.author_model import Author
from book.models.book_language_model import BookLanguage
from book.models.book_level_model import BookLevel
from book.models.category_model import Category
from book.models.book_model import Book
import json
from quiz.models import Question
from quiz.models.quiz_model import Quiz
from django.utils.translation import activate
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class QuestionTests(APITestCase):
    activate('en')
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
        self.question = Question.objects.create(quiz = self.quiz, question = "Example Question 1", topic = "Example topic 1")
        self.url = reverse("quiz:get_questions_by_quiz_id", kwargs= {"quiz_id": self.quiz.id})
        self.url_enabled = reverse("quiz:get_questions_by_enabled_quiz_id", kwargs= {"quiz_id": self.quiz.id})
        self.url_single = reverse("quiz:get_question_by_id", kwargs= {"id": self.question.id})
        self.url_single_book = reverse("quiz:get_last_enabled_quiz_by_book_id", kwargs= {"book_id": self.book.id})


    def test_jwt_authentication(self, username="johndoe", password="test1234"):
        response = self.client.post(self.login_url, data={"username": username, "password": password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_get_questions_by_quiz_id_is_authenticated(self):
        """
            To see the question, the person must be logged in. 
        """
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_get_questions_by_quiz_id(self):
        """
            This unit test will check whether the GetQuestionByQuiz page returns status code 200.
        """
        self.test_jwt_authentication()
        response2 = self.client.get(self.url)
        self.assertEqual(200, response2.status_code)

    def test_get_questions_by_enabled_quiz_id_is_authenticated(self):
        """
            To see the question, the person must be logged in. 
        """
        response = self.client.get(self.url_enabled)
        self.assertEqual(401, response.status_code)

    def test_get_questions_by_enabled_quiz_id(self):
        """
            This unit test will check whether the GetQuestionByEnabledQuiz page returns status code 404.
            The second stage of this test checks if the results page returns a status code of 200 when the "enabled" option of the test is checked as true.
        """
        self.quiz.enabled = False
        self.quiz.save()
        self.test_jwt_authentication()
        response = self.client.get(self.url_enabled)
        self.assertEqual(404, response.status_code)
        self.quiz.enabled = True
        self.quiz.save()
        response2 = self.client.get(self.url_enabled)
        self.assertEqual(200, response2.status_code)

    def test_get_questions_by_id_is_authenticated(self):
        """
            To see the question, the person must be logged in to see the GetQuestionByQuestionId Page. 
        """
        response = self.client.get(self.url_single)
        self.assertEqual(401, response.status_code)
        self.test_jwt_authentication()
        response2 = self.client.get(self.url_single)
        self.assertEqual(200, response2.status_code)

    def test_get_last_enabled_quiz_by_book_id_is_authenticated(self):
        """
            To see the question, the person must be logged in to see the GetLastQuizByBookId Page. 
        """
        response = self.client.get(self.url_single_book)
        self.assertEqual(401, response.status_code)
        self.test_jwt_authentication()
        response2 = self.client.get(self.url_single_book)
        self.assertEqual(200, response2.status_code)

    def test_get_last_enabled_quiz_by_book_id(self):
        """
            This unit test will check whether the GetLastQuizByBookId page returns status code 200 but book field must be null.
            The second stage of this test checks if the results page returns a status code of 200 when the "enabled" option of the test is checked as true.
        """
        self.quiz.enabled = False
        self.quiz.save()
        self.test_jwt_authentication()
        response = self.client.get(self.url_single_book)
        self.assertEqual(200, response.status_code)
        self.assertTrue("None" in str(json.loads(response.content)["book"]))
        self.quiz.enabled = True
        self.quiz.save()
        response2 = self.client.get(self.url_single_book)
        self.assertEqual(200, response2.status_code)
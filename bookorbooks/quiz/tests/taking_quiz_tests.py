from school.models.student_list_model import StudentList
from school.models.class_model import Class
from country.models.city_model import City
from country.models.country_model import Country
from school.models.school_model import School
from account.models.child_list_model import ChildList
from account.models.child_profile_model import ChildProfile
from quiz.models.taking_quiz_answer_model import TakingQuizAnswer
from quiz.models.taking_quiz_model import TakingQuiz
from quiz.models.question_model import Question
from book.models.reading_history_model import ReadingHistory
from book.models.author_model import Author
from book.models.book_language_model import BookLanguage
from book.models.book_level_model import BookLevel
from book.models.category_model import Category
from book.models.book_model import Book
import json
from quiz.models.answer_model import Answer
from quiz.models.quiz_model import Quiz
from django.utils.translation import activate
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TakingQuizAndTakingQuizAnswerTests(APITestCase):
    activate('en')
    url_history_by_parent = reverse("quiz:get_children_quiz_history")
    url_history_by_instructor = reverse("quiz:get_students_quiz_history")
    url_history_by_child = reverse("quiz:get_quiz_history_by_child")
    login_url = reverse("token_obtain_pair")

    def setUp(self) -> None:
        #users
        self.password = "test1234"
        self.user_parent = User.objects.create_user(username="johndoe", password=self.password, email="johndoe@example.com", identity_number="1", user_type=3)
        self.user_instructor = User.objects.create_user(username="davedoe", password=self.password, email="davedoe@example.com", identity_number="2", user_type=4)
        self.user_instructor2 = User.objects.create_user(username="jackdoe", password=self.password, email="jackdoe@example.com", identity_number="4", user_type=4)
        self.user_child = User.objects.create_user(username="janedoe", password=self.password, email="janedoe@example.com", identity_number="3", user_type=2, first_name = "jane")

        #book
        self.category = Category.objects.create(title="Category Title", description="Category description")
        self.book_level = BookLevel.objects.create(title="A")
        self.book_language = BookLanguage.objects.create(language_name="Language Name", language_code="Language Code")
        self.author = Author.objects.create(first_name="Author", last_name="Doe", biography="Example bio")
        self.book = Book.objects.create(level=self.book_level, category=self.category, author=self.author, language=self.book_language, name="Book Name 1", description="Book description")

        #city
        self.country = Country.objects.create(name = "Türkiye", code = "Tur")
        self.city = City.objects.create(country = self.country, name = "Konya", code = "42")

        #child list
        self.child_list = ChildList.objects.create(parent = self.user_parent.user_parent, child = self.user_child.user_child)

        #student list
        self.school = School.objects.create(city = self.city, name = "Example school", address = "Example address", website = "example website")
        self.school_class = Class.objects.create(school = self.school, instructor = self.user_instructor.user_instructor, name = "Class A", grade = 3)
        self.student_list = StudentList.objects.create(school_class = self.school_class, child = self.user_child.user_child)

        #reading history
        self.reading_history = ReadingHistory.objects.create(book = self.book, child = self.user_child.user_child, is_finished = True, counter = 1)

        #quiz
        self.quiz = Quiz.objects.create(book=self.book, title="Example Quiz 1", enabled=True)
        self.question = Question.objects.create(quiz = self.quiz, question = "Example Question", topic = "Example topic")
        self.answer = Answer.objects.create(question = self.question, answer = "Example answer", is_correct = True)
        self.taking_quiz = TakingQuiz.objects.create(quiz = self.quiz, child = self.user_child.user_child, total_point = 100)
        self.taking_quiz_answer = TakingQuizAnswer.objects.create(taking_quiz = self.taking_quiz, question = self.question, answer = self.answer)

        self.url_history_by_class_id = reverse("quiz:get_students_quiz_history_by_class", kwargs={"class_id" : self.school_class.id})


    def test_jwt_authentication(self, username="johndoe", password="test1234"):
        response = self.client.post(self.login_url,
                                    data={
                                        "username": username,
                                        "password": password
                                    })
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_taking_quiz_history_by_parent_is_authenticated(self):
        """
            To see that page, user must be logged in.
        """
        response = self.client.get(self.url_history_by_parent)
        self.assertEqual(401, response.status_code)
    
    def test_taking_quiz_history_by_parent_is_parent(self):
        """
            To see that page, user must be a parent.
        """
        self.test_jwt_authentication(username="davedoe")
        response = self.client.get(self.url_history_by_parent)
        self.assertEqual(403, response.status_code)
    
    def test_taking_quiz_history_by_parent(self):
        """
            This test checks that if GetQuizHistoryByParent view is working correctly.
        """
        self.test_jwt_authentication(username="johndoe")
        response = self.client.get(self.url_history_by_parent)
        self.assertEqual(200, response.status_code)

    def test_taking_quiz_history_by_instructor_is_authenticated(self):
        """
            To see that page, user must be logged in.
        """
        response = self.client.get(self.url_history_by_instructor)
        self.assertEqual(401, response.status_code)
    
    def test_taking_quiz_history_by_instructor_is_instructor(self):
        """
            To see that page, user must be an instructor.
        """
        self.test_jwt_authentication(username="johndoe")
        response = self.client.get(self.url_history_by_instructor)
        self.assertEqual(403, response.status_code)
    
    def test_taking_quiz_history_by_instructor(self):
        """
            This test checks that if GetQuizHistoryByInstructor view is working correctly.
        """
        self.test_jwt_authentication(username="davedoe")
        response = self.client.get(self.url_history_by_instructor)
        self.assertEqual(200, response.status_code)
    
    def test_taking_quiz_history_by_class_id_is_authenticated(self):
        """
            To see that page, user must be logged in.
        """
        response = self.client.get(self.url_history_by_class_id)
        self.assertEqual(401, response.status_code)
    
    def test_taking_quiz_history_by_class_id_is_instructor(self):
        """
            To see that page, user must be an instructor.
        """
        self.test_jwt_authentication(username="johndoe")
        response = self.client.get(self.url_history_by_class_id)
        self.assertEqual(403, response.status_code)
    
    def test_taking_quiz_history_by_class_id_is_own_class(self):
        """
            To see that page, user must be the instructor of that class.
        """
        self.test_jwt_authentication(username="jackdoe")
        response = self.client.get(self.url_history_by_class_id)
        self.assertEqual(403, response.status_code)
    
    def test_taking_quiz_history_by_class_id(self):
        """
            This test checks that if GetQuizHistoryByClassId view is working correctly.
        """
        self.test_jwt_authentication(username="davedoe")
        response = self.client.get(self.url_history_by_class_id)
        self.assertEqual(200, response.status_code)

    def test_taking_quiz_history_by_child_is_authenticated(self):
        """
            To see that page, user must be logged in.
        """
        response = self.client.get(self.url_history_by_child)
        self.assertEqual(401, response.status_code)
    
    def test_taking_quiz_history_by_child_is_child(self):
        """
            To see that page, user must be a child.
        """
        self.test_jwt_authentication(username="johndoe")
        response = self.client.get(self.url_history_by_child)
        self.assertEqual(403, response.status_code)
    
    def test_taking_quiz_history_by_child(self):
        """
            This test checks that if TakingQuizListByChild view is working correctly.
        """
        self.test_jwt_authentication(username="janedoe")
        response = self.client.get(self.url_history_by_child)
        self.assertEqual(200, response.status_code)


class TakingQuizCreateTests(APITestCase):
    activate('en')
    url_create = reverse("quiz:create_taking_quiz")
    url_answer = reverse("quiz:create_taking_quiz_answer")
    login_url = reverse("token_obtain_pair")

    def setUp(self) -> None:
        #users
        self.password = "test1234"
        self.user_child = User.objects.create_user(username="johndoe", password=self.password, email="johndoe@example.com", identity_number="1", user_type=2)
        
        #book
        self.category = Category.objects.create(title="Category Title", description="Category description")
        self.book_level = BookLevel.objects.create(title="A")
        self.book_language = BookLanguage.objects.create(language_name="Language Name", language_code="Language Code")
        self.author = Author.objects.create(first_name="Author", last_name="Doe", biography="Example bio")
        self.book = Book.objects.create(level=self.book_level, category=self.category, author=self.author, language=self.book_language, name="Book Name 1", description="Book description")

        #reading history
        self.reading_history = ReadingHistory.objects.create(book = self.book, child = self.user_child.user_child, is_finished = True, counter = 1)

        #quiz
        self.quiz = Quiz.objects.create(book=self.book, title="Example Quiz 1", enabled=True)
        self.question = Question.objects.create(quiz = self.quiz, question = "Example Question", topic = "Example topic")
        self.answer = Answer.objects.create(question = self.question, answer = "Example answer", is_correct = True)
        self.taking_quiz = TakingQuiz.objects.create(quiz = self.quiz, child = self.user_child.user_child, total_point = 100)
        self.taking_quiz_answer = TakingQuizAnswer.objects.create(taking_quiz = self.taking_quiz, question = self.question, answer = self.answer)

        #fake quiz data
        self.quiz2 = Quiz.objects.create(book=self.book, title="Example Quiz 2", enabled=True)
        self.question2 = Question.objects.create(quiz = self.quiz2, question = "Example Question 2", topic = "Example topic 2")
        self.answer2 = Answer.objects.create(question = self.question2, answer = "Example answer 2", is_correct = True)

        self.url_update = reverse("quiz:update_taking_quiz", kwargs={"id": self.taking_quiz.id})


    def test_jwt_authentication(self, username="johndoe", password="test1234"):
        response = self.client.post(self.login_url, data={"username": username, "password": password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_taking_quiz_create_is_authenticated(self):
        """
            To see this page, user must be logged in.
        """
        response = self.client.get(self.url_create)
        self.assertEqual(401, response.status_code)
    
    def test_taking_quiz_create_is_child(self):
        """
            To see this page, user must be a child.
        """
        self.user_child.user_type = 1
        self.user_child.save()
        self.test_jwt_authentication()
        response = self.client.get(self.url_create)
        self.assertEqual(403, response.status_code)

    def test_taking_quiz_create_is_reading_finished(self):
        """
            To create a user quiz record, a reading record about that book and child must have in reading history table. And the is_finished field of that record must be selected True.
        """
        self.reading_history.is_finished = False
        self.reading_history.save()
        self.test_jwt_authentication()
        data = {
            "quiz" : self.quiz.id,
            "child" : self.user_child.id,
            "total_point" : 100,
        }
        response = self.client.post(self.url_create, data = data)
        self.assertEqual(403, response.status_code)
    
    def test_taking_quiz_create(self):
        """
            This unit test checks that whether the record of a taking quiz created successfully. 
        """
        self.test_jwt_authentication()
        data = {
            "quiz" : self.quiz.id,
            "child" : self.user_child.id,
            "total_point" : 100,
        }
        response = self.client.post(self.url_create, data = data)
        self.assertEqual(201, response.status_code)

    def test_taking_quiz_update_is_authenticated(self):
        """
            To see this page, user must be logged in.
        """
        response = self.client.get(self.url_update)
        self.assertEqual(401, response.status_code)
    
    def test_taking_quiz_update_is_child(self):
        """
            To see this page, user must be a child.
        """
        self.user_child.user_type = 1
        self.user_child.save()
        self.test_jwt_authentication()
        response = self.client.get(self.url_update)
        self.assertEqual(403, response.status_code)

    def test_taking_quiz_update(self):
        """
            This unit test checks that whether the record of taking quiz updated successfully. 
        """
        self.test_jwt_authentication()
        data = {
            "quiz": self.quiz.id,
            "total_point" : 70,
        }
        response = self.client.put(self.url_update, data = data)
        self.assertEqual(200, response.status_code)
    
    def test_taking_quiz_answer_create_is_authenticated(self):
        """
            To see this page, user must be logged in.
        """
        response = self.client.get(self.url_answer)
        self.assertEqual(401, response.status_code)
    
    def test_taking_quiz_answer_create_is_child(self):
        """
            To see this page, user must be a child.
        """
        self.user_child.user_type = 1
        self.user_child.save()
        self.test_jwt_authentication()
        response = self.client.get(self.url_answer)
        self.assertEqual(403, response.status_code)

    def test_taking_quiz_answer_answer_is_not_belong_question(self):
        """
            Checks that whether the answer belongs to the question.
        """
        data = {
            "taking_quiz": self.taking_quiz.id,
            "question": self.question.id,
            "answer": self.answer2.id
        }
        self.test_jwt_authentication()
        response = self.client.post(self.url_answer, data = data)
        self.assertEqual(403, response.status_code)
    
    def test_taking_quiz_answer_answer_is_not_belong_question(self):
        """
            Checks that whether the question belongs to the quiz.
        """
        data = {
            "taking_quiz": self.taking_quiz.id,
            "question": self.question2.id,
            "answer": self.answer.id
        }
        self.test_jwt_authentication()
        response = self.client.post(self.url_answer, data = data)
        self.assertEqual(403, response.status_code)

    def test_taking_quiz_answer_create(self):
        """
            This unit test checks that whether the record of taking quiz answer created successfully. 
        """
        self.test_jwt_authentication()
        data = {
            "taking_quiz": self.taking_quiz.id,
            "question": self.question.id,
            "answer": self.answer.id
        }
        response = self.client.post(self.url_answer, data = data)
        self.assertEqual(201, response.status_code)
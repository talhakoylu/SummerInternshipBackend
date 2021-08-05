from account.models.instructor_model import InstructorProfile
import json
from school.models.class_model import Class
from school.models.school_model import School
from django.urls.base import reverse
from rest_framework.test import APITestCase
from country.models import Country, City
from django.contrib.auth import get_user_model

User = get_user_model()

class ClassTests(APITestCase):
    url_list = reverse("school:list_class")
    url_create = reverse("school:add_class")
    url_login = reverse("token_obtain_pair")

    def setUp(self) -> None:
        self.country = Country.objects.create(name = "Türkiye", code = "Tur")
        self.city = City.objects.create(country = self.country, name = "Konya", code = "42")
        self.school = School.objects.create(city = self.city, name = "Example School", address = "Example Address", website = "Example website")
        self.create_instructor(school=self.school)
        self.create_class(school_class = self.school ,user = self.user.user_instructor, name = "Class A", grade = 4)
        self.url_update = reverse("school:update_class", kwargs={"id" : self.school_class.id})
        self.fake_user_data = {
            "username" : "johndoetest",
            "password" : "johndoe123",
            "user_type" : 3
        }
        self.fake_user = User.objects.create_user(username = self.fake_user_data["username"], password = self.fake_user_data["password"], 
        user_type = self.fake_user_data["user_type"], email = "johndoetest@example.com", identity_number = "12345678910")

    def create_instructor(self, school, username = "johndoe", password = "johndoe123", user_type = 4):
        self.login_data = {
            username : username,
            password : password
        }
        self.user = User.objects.create_user(username = username, password = password, user_type = user_type)
        instructor = InstructorProfile.objects.get(user = self.user)
        instructor.school = school
        instructor.save()

    def create_class(self, school_class, user, name, grade):
        self.school_class = Class.objects.create(instructor = user, school = school_class, name = name, grade = grade)

    def login_with_token(self, login_data):
        """
            A method for using login process.
        """
        response = self.client.post(self.url_login, login_data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_get_class_list(self):
        """
            Tests that class list page returns a status code of 200 and whether the details contains city, country and name fields.
        """
        response = self.client.get(self.url_list)
        result = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertTrue("school" in result[0] and result[0]["school"]["name"] == "Example School")
        self.assertTrue("instructor" in result[0])
        self.assertTrue("name" in result[0] and result[0]["name"] == "Class A")
        
    def test_create_class_is_authenticated(self):
        """
            Tests whether the user is authenticated, and if not, the user cannot access the "class add" page.
        """
        response = self.client.get(self.url_create)
        self.assertEqual(401, response.status_code)

    def test_create_class_is_instructor(self):
        """
            Tests whether the user is instructor.
        """
        self.login_with_token(self.fake_user_data)
        response = self.client.get(self.url_create)
        self.assertEqual(403, response.status_code)

    def test_class_update_is_authenticated(self):
        """
            Tests whether the user is authenticated, and if not, the user cannot access the "class update" page.
        """
        response = self.client.get(self.url_update)
        self.assertEqual(401, response.status_code)

    def test_class_update_is_instructor(self):
        """
            Tests whether the user is instructor.
        """
        self.login_with_token(self.fake_user_data)
        response = self.client.get(self.url_create)
        self.assertEqual(403, response.status_code)
    
    def test_class_update_is_own_class(self):
        """
            Tests whether the user is instructor.
        """
        self.fake_user_data["user_type"] = 4
        self.login_with_token(self.fake_user_data)
        response = self.client.get(self.url_create)
        self.assertEqual(403, response.status_code)
        self.assertTrue("detail" in json.loads(response.content))

    def test_class_create(self):
        """
            Class createcls page test.
        """
        class_data = {
            "name": "Class Name",
            "grade" : 8
        }
        
        login = {
            "username": "johndoe",
            "password" : "johndoe123"
        }

        self.login_with_token(login)
        response = self.client.post(self.url_create, class_data)
        result = Class.objects.filter(instructor=self.user.user_instructor)
        self.assertEqual(201, response.status_code)
        self.assertTrue(result.count() > 0)
        

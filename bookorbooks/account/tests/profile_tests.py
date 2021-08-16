from country.models.country_model import Country
from country.models.city_model import City
import json
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from school.models import School

User = get_user_model()


class ChildProfileTests(APITestCase):
    url = reverse("account:child_profile_update")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "johndoe"
        self.password = "pass1234"
        self.user_type = 2
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password,
                                             user_type=self.user_type)
        self.login_data = {
            "username": self.username,
            "password": self.password
        }
        self.country = Country.objects.create(name="Türkiye", code="Tur")
        self.city = City.objects.create(country=self.country,
                                        name="Konya",
                                        code="42")
        self.profile_data = {
            "id": self.user.id,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "identity_number": "23456892138",
            "gender": 1,
            "birth_date": "1999-12-11",
            "user_child": {
                "city": self.city.id,
                "district": None,
                "hobbies": "example hobbies"
            }
        }

    def login_with_token(self):
        """
            A method for using login process. The main purpose of this code is to avoid code repeat.
        """
        response = self.client.post(self.url_login, self.login_data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_is_authenticated_user(self):
        """
            Tests that the user cannot access the password update page if user isn't authenticated.
        """
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_wrong_user_type(self):
        """
            Checks if the user type is child or not.
        """
        self.user.user_type = 4
        self.user.save()
        self.login_with_token()
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)
        self.assertTrue("detail" in json.loads(response.content))

    def test_with_valid_informations(self):
        """
            Tests that user can change user and profile fields with correct values.
        """
        self.login_with_token()
        response = self.client.put(self.url, self.profile_data, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content), self.profile_data)


class ParentProfileTests(APITestCase):
    url = reverse("account:parent_profile_update")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "johndoe"
        self.password = "pass1234"
        self.user_type = 3
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password,
                                             user_type=self.user_type)
        self.login_data = {
            "username": self.username,
            "password": self.password
        }
        self.country = Country.objects.create(name="Türkiye", code="Tur")
        self.city = City.objects.create(country=self.country,
                                        name="Konya",
                                        code="42")
        self.profile_data = {
            "id": self.user.id,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "identity_number": "23456892138",
            "gender": 1,
            "birth_date": "1999-12-11",
            "user_parent": {
                "city": self.city.id,
                "district": None,
                "profession": "example profession"
            }
        }

    def login_with_token(self):
        """
            A method for using login process. The main purpose of this code is to avoid code repeat.
        """
        response = self.client.post(self.url_login, self.login_data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_is_authenticated_user(self):
        """
            Tests that the user cannot access the password update page if user isn't authenticated.
        """
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_wrong_user_type(self):
        """
            Checks if the user type is child or not.
        """
        self.user.user_type = 4
        self.user.save()
        self.login_with_token()
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)
        self.assertTrue("detail" in json.loads(response.content))

    def test_with_valid_informations(self):
        """
            Tests that user can change user and profile fields with correct values.
        """
        self.login_with_token()
        response = self.client.put(self.url, self.profile_data, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content), self.profile_data)


class InstructorProfileTests(APITestCase):
    url = reverse("account:instructor_profile_update")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "johndoe"
        self.password = "pass1234"
        self.user_type = 4
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password,
                                             user_type=self.user_type)
        self.login_data = {
            "username": self.username,
            "password": self.password
        }
        self.country = Country.objects.create(name="Türkiye", code="Tur")
        self.city = City.objects.create(country=self.country,
                                        name="Konya",
                                        code="42")
        self.school = School.objects.create(city=self.city,
                                            name="Example School",
                                            address="Address",
                                            website="webisite.com")
        self.profile_data = {
            "id": self.user.id,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "identity_number": "23456892138",
            "gender": 1,
            "birth_date": "1999-12-11",
            "user_instructor": {
                "school": self.school.id,
                "branch": "example branch"
            }
        }

    def login_with_token(self):
        """
            A method for using login process. The main purpose of this code is to avoid code repeat.
        """
        response = self.client.post(self.url_login, self.login_data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_is_authenticated_user(self):
        """
            Tests that the user cannot access the password update page if user isn't authenticated.
        """
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_wrong_user_type(self):
        """
            Checks if the user type is child or not.
        """
        self.user.user_type = 2
        self.user.save()
        self.login_with_token()
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)
        self.assertTrue("detail" in json.loads(response.content))

    def test_with_valid_informations(self):
        """
            Tests that user can change user and profile fields with correct values.
        """
        self.login_with_token()
        response = self.client.put(self.url, self.profile_data, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content), self.profile_data)
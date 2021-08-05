from django.utils.translation import activate
from account.models.parent_profile_model import ParentProfile
from account.models.child_profile_model import ChildProfile
import json
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserRegistrationTests(APITestCase):
    activate('en')
    url = reverse("account:register")
    url_login = reverse("token_obtain_pair")

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(first_name="John",
                                              last_name="Doe",
                                              email="johndoe@example.com",
                                              username="johndoe",
                                              password="Pas12wor21d",
                                              identity_number="12345678910",
                                              user_type=2,
                                              gender=1)

        self.data = {
            "username": "johndoe1",
            "email": "johndoe1@example.com",
            "password": "johndoe123",
            "identity_number": "12345678913",
            "user_type": 2,
            "gender": 1,
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": "2000-07-26"
        }

    def test_user_registration(self):
        """
            User registration with correct values
        """

        response = self.client.post(self.url, self.data)
        self.assertEqual(201, response.status_code)

    def test_invalid_password(self):
        """
            User registration with invalid password
        """

        self.data["password"] = "123"

        response = self.client.post(self.url, self.data)
        self.assertEqual(400, json.loads(response.content)["status_code"])

    def test_unique_fields(self):
        """
            Check unique field validations are working correctly for username, email and identity_number fields.
        """
        data2 = {
            "username": "johndoe",
            "email": "johndoe@example.com",
            "password": "johndoe123",
            "identity_number": "12345678910",
            "user_type": 2,
            "gender": 1,
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": "2000-07-26"
        }

        response = self.client.post(self.url, data2)
        assert 400 == json.loads(response.content)["status_code"]
        self.assertTrue("email" in json.loads(response.content))
        self.assertTrue("username" in json.loads(response.content))
        self.assertTrue("identity_number" in json.loads(response.content))

    def test_authenticated_user_register_page(self):
        """
            Authenticated user cannot access the registration page.
        """
        self.test_user_registration()
        self.client.login(username=self.data["username"],
                          password=self.data["password"])
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)

    def test_token_user_register_page(self):
        """
            Tests that the user cannot access the page if logged in with token.
        """
        self.test_user_registration()

        data = {
            "username": self.data["username"],
            "password": self.data["password"]
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response_2 = self.client.get(self.url)
        self.assertEqual(403, response_2.status_code)

    def test_profile_null_fields(self):
        """
            Checks that not nullable fields.
        """
        self.data["identity_number"] = ""
        self.data["gender"] = ""
        self.data["email"] = ""
        self.data["user_type"] = ""
        self.data["gender"] = ""
        self.data["username"] = ""
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(400, response.status_code)

    def test_profile_change_test(self):
        """
            Tests the existence of records in the relevant tables according to whether the user type has changed.
        """
        child_profile_exists = ChildProfile.objects.filter(
            user=self.user1).exists()
        self.assertTrue(child_profile_exists)
        self.user1.user_type = 3
        self.user1.save()
        child_profile_not_exists = ChildProfile.objects.filter(
            user=self.user1).exists()
        self.assertFalse(child_profile_not_exists)
        parent_profile_exists = ParentProfile.objects.filter(
            user=self.user1).exists()
        self.assertTrue(parent_profile_exists)


class CustomUserLoginTests(APITestCase):
    activate('en')
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "johndoe"
        self.password = "Pas12wor21d"
        self.user1 = User.objects.create_user(first_name="John",
                                              last_name="Doe",
                                              email="johndoe@example.com",
                                              username=self.username,
                                              password=self.password,
                                              identity_number="12345678910",
                                              user_type="2",
                                              gender=1)

    def test_user_token(self):
        """
            Tests whether the user authentication token has been created correctly. 
        """
        response = self.client.post(self.url_login, {
            "username": self.username,
            "password": self.password
        })
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))

    def test_user_invalid_data(self):
        """
            Tests whether the user can log in with incorrect information. 
        """
        response = self.client.post(self.url_login, {
            "username": "asasdzxczxc",
            "password": "pass1234"
        })
        self.assertEqual(401, response.status_code)

    def test_user_empty_data(self):
        """
            Tests whether the user can log in with empty data.
        """
        response = self.client.post(self.url_login, {
            "username": "",
            "password": ""
        })
        self.assertEqual(400, response.status_code)


class CustomUserPasswordChange(APITestCase):
    activate('en')
    url = reverse("account:update_password")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "johndoe"
        self.password = "pass1234"
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
        self.login_data = {
            "username": self.username,
            "password": self.password
        }  # login data
        self.change_data = {
            "old_password": self.password,
            "new_password": "test-password-12"
        }  # password changing data, true by default.

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

    def test_with_valid_informations(self):
        """
            Tests that user can change the password with correct values and checks that the response is contains success or not.
        """
        self.login_with_token()
        response = self.client.put(self.url, self.change_data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("success" in json.loads(response.content)["status"])

    def test_with_wrong_informations(self):
        self.login_with_token()
        self.change_data["old_password"] = "wrong-password"
        response = self.client.put(self.url, self.change_data)
        self.assertEqual(400, response.status_code)

    def test_with_empty_informations(self):
        """
            Tests that the user cannot change password or send request if the fields are empty.
        """
        self.login_with_token()
        self.change_data["old_password"] = ""
        self.change_data["new_password"] = ""
        response = self.client.put(self.url, self.change_data)
        self.assertEqual(400, response.status_code)
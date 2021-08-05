from django.utils.translation import activate
from account.models.child_list_model import ChildList
from account.models.child_profile_model import ChildProfile
from account.models.parent_profile_model import ParentProfile
import json
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class ChildListTests(APITestCase):
    activate('en')
    url = reverse("account:child_list")
    url_by_parent = reverse("account:child_list_detail")
    url_add = reverse("account:child_list_create")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username1 = "johndoechild"
        self.password1 = "pass1234"
        self.user_type1 = 2
        self.child_user = User.objects.create_user(
            username=self.username1,
            password=self.password1,
            user_type=self.user_type1,
            first_name="John",
            last_name="Doe Child",
            email="childdoe@example.com",
            identity_number="12345678910")

        self.login_data_child = {
            "username": self.username1,
            "password": self.password1
        }

        self.username2 = "johndoeparent"
        self.password2 = "pass1234"
        self.user_type2 = 3
        self.parent_user = User.objects.create_user(
            username=self.username2,
            password=self.password2,
            user_type=self.user_type2,
            first_name="John",
            last_name="Doe Parent",
            email="parentdoe@example.com",
            identity_number="12345678911")
        
        self.login_data_parent = {
            "username": self.username2,
            "password": self.password2
        }

        
        self.username3 = "johndoeparent2"
        self.password3 = "pass1234"
        self.user_type3 = 3
        self.parent_user2 = User.objects.create_user(
            username=self.username3,
            password=self.password3,
            user_type=self.user_type3,
            first_name="John",
            last_name="Doe Parent",
            email="parentdoe2@example.com",
            identity_number="12345678913")

        self.login_data_parent2 = {
            "username": self.username3,
            "password": self.password3
        }


    def parent_login_with_token(self, login_data):
        """
            A method for using login process. The main purpose of this code is to avoid code repeat.
        """
        response = self.client.post(self.url_login, login_data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_child_list_get_all(self):
        """
            A unit test that controls if all parent-child relations are returned.
        """
        response = self.client.get(self.url)
        assert 200 == response.status_code

    def test_child_list_create_is_authenticated(self):
        """
            Tests whether the user is authenticated, and if not, the user cannot access the "child record add" page.
        """
        response = self.client.get(self.url_add)
        assert 401 == response.status_code

    def test_child_list_create_is_parent(self):
        """
            Tests whter the user is parent.
        """
        self.client.login(username=self.login_data_child["username"],
                          password=self.login_data_child["password"])
        response = self.client.get(self.url_add)
        assert 403 == response.status_code

    def test_child_record_add(self):
        """
            Parent-child relation record add page test.
        """
        self.parent_login_with_token(self.login_data_parent)
        data = {"parent": self.parent_user.id, "child": self.child_user.id}

        response = self.client.post(self.url_add, data)
        result = ChildList.objects.filter(parent=self.parent_user.user_parent)
        self.assertEqual(201, response.status_code)
        self.assertTrue(result.count() > 0)

    def test_child_list_by_parent(self):
        """
            Child list detail page shows the result by authenticated parent. This test checks that the user has a child and wheter the child informations are correct.
        """
        self.test_child_record_add()
        response = self.client.get(self.url_by_parent)
        self.assertEqual(200, response.status_code)
        self.assertTrue("children" in json.loads(response.content)
                        and json.loads(response.content)["children"][0]
                        ["child"]["user"]["get_full_name"] == "John Doe Child")

    def test_destroy_child_list_item_is_authenticated(self):
        """
            Tests whether the user is authenticated, and if not, the user cannot access the "child list item destroy" page.
        """
        url = reverse("account:child_list_item_destroy", kwargs={"child_id": self.child_user.id})
        response = self.client.get(url)
        assert 401 == response.status_code

    def test_destroy_child_list_item_is_parent(self):
        """
            Tests whether the user is parent.
        """
        self.client.login(username=self.login_data_child["username"],
                          password=self.login_data_child["password"])
        response = self.client.get(self.url_add)
        assert 403 == response.status_code



class ChildListItemDestroyTests(APITestCase):
    activate('en')
    login_url = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "johndoe"
        self.password = "test1234"
        self.user_parent = User.objects.create_user(username=self.username, password=self.password, email = "email1@example.com", identity_number = "12345678910", user_type = 3)
        self.user_parent2 = User.objects.create_user(username= "davedoe", password=self.password, email = "email3@example.com", identity_number = "12345678912", user_type = 3)
        self.user_child = User.objects.create_user(username="janedoe", password=self.password, email = "email2@example.com", identity_number = "12345678911", user_type = 2)
        self.child_list_item = ChildList.objects.create(parent = self.user_parent.user_parent, child = self.user_child.user_child)
        self.test_jwt_authentication()

    def test_jwt_authentication(self, username="johndoe", password="test1234"):
        response = self.client.post(self.login_url, data={"username": username, "password": password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
  
    def test_child_list_item_delete(self):
        url = reverse("account:child_list_item_destroy", kwargs={"child_id": self.user_child.user_child.user_id})
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
   
   
    def test_child_list_item_delete_is_own_child(self):
        self.test_jwt_authentication(username = "davedoe")
        url = reverse("account:child_list_item_destroy", kwargs={"child_id": self.user_child.user_child.user_id})
        response = self.client.delete(url)
        self.assertEqual(403, response.status_code)
from school.models.class_model import Class
from account.models.instructor_model import InstructorProfile
from country.models.country_model import Country
from country.models.city_model import City
from school.models.school_model import School
from django.urls.base import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class StudentListTests(APITestCase):
    url_list = reverse("school:student_list")
    url_add = reverse("school:add_student_list_item")
    url_list_by_instructor = reverse("school:student_list_by_class_instructor")
    url_login = reverse("token_obtain_pair")

    def setUp(self) -> None:
        self.country = Country.objects.create(name = "Türkiye", code = "Tur")
        self.city = City.objects.create(country = self.country, name = "Konya", code = "42")
        self.school = School.objects.create(city = self.city, name = "Example School", address = "Example Address", website = "Example website")
        self.password = "testpass123"
        self.normal_user = User.objects.create_user(username = "normaldoe", password = self.password, user_type = 1)
        self.instructor_user1 = User.objects.create_user(
            username="johndoe",
            password=self.password,
            user_type=4,
            email = "johndoe@example.com",
            identity_number = "12345678910",
        )
        instructor_profile = InstructorProfile.objects.get(user = self.instructor_user1)
        instructor_profile.school = self.school
        instructor_profile.save()
        self.instructor_user2 = User.objects.create_user(
            username="johndoe2",
            password=self.password,
            user_type=4,
            email = "johndoe2@example.com",
            identity_number = "12345678911",
        )
        instructor_profile2 = InstructorProfile.objects.get(user = self.instructor_user2)
        instructor_profile2.school = self.school
        instructor_profile2.save()
        self.school_class = Class.objects.create(school = self.school, instructor = self.instructor_user1.user_instructor, name = "Class A", grade = 1)
        self.child = User.objects.create_user(
            username = "johndoechild", 
            password = self.password, 
            email = "childdoe@example.com", 
            identity_number = "12345678912", 
            user_type = 2
        )
        self.url_destroy = reverse("school:student_list_item_destroy", kwargs={"class_id": self.school_class.id, "child_id": self.child.id})

    def login_with_token(self, login_data):
        """
            A method for using login process.
        """
        response = self.client.post(self.url_login, login_data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_student_list(self):
        """
            Tests that school list page returns a status code of 200.
        """
        response = self.client.get(self.url_list)
        self.assertEqual(200, response.status_code)

    def test_add_item_is_authenticated(self):
        """
            Tests whether the user is authenticated.
        """
        response = self.client.get(self.url_add)
        self.assertEqual(401, response.status_code)

    def test_add_item_is_instructor(self):
        """
            Tests whether the user is instructor.
        """
        data = {
            "username": self.normal_user.username,
            "password": self.password
        }
        self.login_with_token(data)
        response = self.client.get(self.url_add)
        self.assertEqual(403, response.status_code)

    def test_add_list_item_is_own_class(self):
        """
            Child-class relation record add page test.
        """
        login_data = {
            "username": self.instructor_user2.username,
            "password": self.password
        }
        self.login_with_token(login_data)
        data = {"school_class": self.school_class.id, "child": self.child.id}

        response = self.client.post(self.url_add, data)
        self.assertEqual(403, response.status_code)
    
    
    def test_add_list_item(self):
        """
            Child-class relation record add page test.
        """
        login_data = {
            "username": self.instructor_user1.username,
            "password": self.password
        }
        self.login_with_token(login_data)
        data = {"school_class": self.school_class.id, "child": self.child.id}

        response = self.client.post(self.url_add, data)
        self.assertEqual(201, response.status_code)

    def test_destroy_student_list_item_is_authenticated(self):
        """
            Tests whether the user is authenticated, and if not, the user cannot access the "student list item destroy" page.
        """
        response = self.client.get(self.url_destroy)
        assert 401 == response.status_code

    def test_destroy_student_list_item_is_instructor(self):
        """
            Tests whether the user is instructor.
        """
        login_data = {
            "username": self.normal_user.username,
            "password": self.password
        }
        self.login_with_token(login_data)
        response = self.client.get(self.url_add)
        assert 403 == response.status_code

    def test_student_list_item_destroy_is_own_class(self):
        """
            This test has to return a 404 result. This is because we used get_object_or_404 in Destroy View. Test user hasn't got any student so this test will return 404.
        """
        login_data = {
            "username": self.instructor_user2.username,
            "password": self.password
        }
        self.login_with_token(login_data)
        response = self.client.delete(self.url_destroy)
        self.assertEqual(404, response.status_code)
    
    def test_student_list_item_destroy(self):
        """
            Tests whether the user can delete class-child relation properly.
        """
        login_data = {
            "username": self.instructor_user1.username,
            "password": self.password
        }
        self.login_with_token(login_data)
        self.test_add_list_item()
        response = self.client.delete(self.url_destroy)
        self.assertEqual(204, response.status_code)
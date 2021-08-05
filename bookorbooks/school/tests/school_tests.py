import json
from school.models.class_model import Class
from school.models.school_model import School
from django.urls.base import reverse
from rest_framework.test import APITestCase
from country.models import Country, City
from django.contrib.auth import get_user_model

User = get_user_model()

class SchoolTests(APITestCase):
    url_list = reverse("school:school_list")

    def setUp(self) -> None:
        self.country = Country.objects.create(name = "Türkiye", code = "Tur")
        self.city = City.objects.create(country = self.country, name = "Konya", code = "42")
        self.school = School.objects.create(city = self.city, name = "Example School", address = "Example Address", website = "Example website")
        self.create_instructor()
        self.create_class(school_class = self.school ,user = self.user.user_instructor, name = "Class A", grade = 4)
        self.url_detail = reverse("school:school_detail", kwargs={"id": self.school.id})

    def create_instructor(self, username = "johndoe", password = "johndoe123", user_type = 4):
        self.user = User.objects.create_user(username = username, password = password, user_type = user_type)

    def create_class(self, school_class, user, name, grade):
        self.school_class = Class.objects.create(instructor = user, school = school_class, name = name, grade = grade)

    def test_get_list(self):
        """
            Tests that school list page returns a status code of 200 and whether the details contains city, country and name fields.
        """
        response = self.client.get(self.url_list)
        self.assertEqual(200, response.status_code)
        self.assertTrue("city" in json.loads(response.content)[0])
        self.assertTrue("country" in json.loads(response.content)[0]["city"])
        self.assertTrue("name" in json.loads(response.content)[0] and json.loads(response.content)[0]["name"] == self.school.name)

    def test_school_detail(self):
        """
            Tests that school detail page by school id returns a status code of 200 and whether the details contains city, country, classes and name fields.
        """
        response = self.client.get(self.url_detail)
        result = json.loads(response.content)
        assert 200 == response.status_code
        self.assertTrue("name" in result and result["name"] == "Example School")
        self.assertTrue("city" in result and result["city"]["name"] == "Konya")
        self.assertTrue("country" in result["city"] and result["city"]["country"]["name"] == "Türkiye")
        self.assertTrue("classes" in result and result["classes"][0]["name"] == "Class A")
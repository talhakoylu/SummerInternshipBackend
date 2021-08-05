from django.utils.translation import activate
from rest_framework.test import APITestCase
from django.urls import reverse
from country.models import City, Country


class CityTests(APITestCase):
    activate('en')
    url = reverse("country:city-list")

    def setUp(self) -> None:
        self.country = Country.objects.create(name="Türkiye", code="Tur")
        self.first_city = City.objects.create(country=self.country,
                                              name="İstanbul",
                                              code="34")

    def test_city_adding(self):
        city = City.objects.create(country=self.country,
                                   name="Konya",
                                   code="42")
        self.assertTrue(City.objects.get(id=city.id))

    def test_city_name_with_code(self):
        city = City.objects.create(country=self.country,
                                   name="Ankara",
                                   code="06")

        test_name = f"{city.name}-{city.code}"
        self.assertEqual(city.get_city_name, test_name)

    def test_foreignkey_value(self):
        city = City.objects.get(code="34")
        self.assertEqual(self.country.id, city.country.id)

    def test_foreignkey_list(self):
        city_list_with_country_id = City.objects.filter(id = self.country.id)
        self.assertTrue(city_list_with_country_id.exists())
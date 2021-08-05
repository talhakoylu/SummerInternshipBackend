from django.utils.translation import activate
from rest_framework.test import APITestCase
from django.urls import reverse
from country.models import Country


class CountryTests(APITestCase):
    activate('en')
    url = reverse("country:country-list")

    def setUp(self) -> None:
        self.country = Country.objects.create(name="Türkiye", code="Tur")

    def test_country_adding(self):
        country2 = Country.objects.create(name="Rusya", code="rus")
        self.assertTrue(Country.objects.get(id=country2.id))

    def test_country_name_with_code(self):
        country = Country.objects.create(name="Amerika Birleşik Devletleri",
                                         code="USA")
        test_name = f"{country.name}-{country.code}"
        self.assertEqual(country.get_country_name_with_code, test_name)

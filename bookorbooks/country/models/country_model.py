from country.models.abstract_country_base_model import AbstractCountryBaseModel
from constants.country_strings import CountryStrings
from django.db import models


class Country(AbstractCountryBaseModel):
    name = models.CharField(
        max_length=150,
        verbose_name=CountryStrings.CountryStrings.name_verbose_name, unique=True)
    code = models.CharField(
        max_length=10,
        verbose_name=CountryStrings.CountryStrings.code_verbose_name, unique=True)

    class Meta:
        verbose_name = CountryStrings.CountryStrings.meta_verbose_name
        verbose_name_plural = CountryStrings.CountryStrings.meta_verbose_name_plural

    @property
    def get_country_name_with_code(self):
        return "{}-{}".format(self.name, self.code)

    def __str__(self):
        return self.get_country_name_with_code

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.code = self.code.upper()
        return super(Country, self).save(*args, **kwargs)
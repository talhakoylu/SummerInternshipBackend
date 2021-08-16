from django.core.exceptions import ValidationError
from country.models.abstract_country_base_model import AbstractCountryBaseModel
from constants.country_strings import CountryStrings
from django.db import models


class City(AbstractCountryBaseModel):
    country = models.ForeignKey(
        "country.Country",
        on_delete=models.CASCADE,
        related_name="cities",
        verbose_name=CountryStrings.CityStrings.country_verbose_name)
    district = models.ForeignKey(
        "country.District",
        on_delete=models.SET_NULL,
        related_name="district_cities",
        verbose_name=CountryStrings.CityStrings.district_verbose_name,
        null=True,
        blank=True)
    name = models.CharField(
        max_length=150,
        verbose_name=CountryStrings.CityStrings.name_verbose_name,
        unique=True)
    code = models.CharField(
        max_length=10,
        verbose_name=CountryStrings.CityStrings.code_verbose_name,
        unique=True)

    class Meta:
        verbose_name = CountryStrings.CityStrings.meta_verbose_name
        verbose_name_plural = CountryStrings.CityStrings.meta_verbose_name_plural

    @property
    def get_city_name(self):
        return "{}-{}".format(self.name, self.code)

    def __str__(self):
        return self.get_city_name

    def clean(self) -> None:
        """
        This method will check if the district of the city is linked to the the country of the city.
        """
        if self.district and self.country and self.district.country != self.country:
            raise ValidationError(CountryStrings.CityStrings.country_validation_error)
        else:
            return True

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.code = self.code.upper()
        return super(City, self).save(*args, **kwargs)
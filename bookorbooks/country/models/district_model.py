from constants.country_strings import CountryStrings
from country.models.abstract_country_base_model import AbstractCountryBaseModel
from django.db import models


class District(AbstractCountryBaseModel):
    country = models.ForeignKey(
        "country.Country",
        on_delete=models.CASCADE,
        related_name="districts",
        verbose_name=CountryStrings.DistrictStrings.country_verbose_name)
    name = models.CharField(
        max_length=150,
        verbose_name=CountryStrings.DistrictStrings.name_verbose_name)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = CountryStrings.DistrictStrings.meta_verbose_name
        verbose_name_plural = CountryStrings.DistrictStrings.meta_verbose_name_plural

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(District, self).save(*args, **kwargs)
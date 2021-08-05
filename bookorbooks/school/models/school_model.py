from constants.school_strings import SchoolStrings
from django.db import models
from school.models.abstract_base_model import AbstractSchoolBaseModel


class School(AbstractSchoolBaseModel):
    city = models.ForeignKey(
        "country.City",
        on_delete=models.DO_NOTHING,
        related_name="city_schools",
        verbose_name=SchoolStrings.SchoolStrings.city_verbose_name)
    name = models.CharField(
        max_length=250,
        verbose_name=SchoolStrings.SchoolStrings.name_verbose_name)
    address = models.CharField(
        max_length=250,
        verbose_name=SchoolStrings.SchoolStrings.address_verbose_name)
    website = models.CharField(
        max_length=250,
        verbose_name=SchoolStrings.SchoolStrings.website_verbose_name)

    class Meta:
        verbose_name = SchoolStrings.SchoolStrings.meta_verbose_name
        verbose_name_plural = SchoolStrings.SchoolStrings.meta_verbose_name_plural

    def __str__(self):
        return self.name
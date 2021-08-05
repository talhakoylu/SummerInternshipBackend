from django.db import models
from constants.book_strings import BookStrings


class AbstractCountryBaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=BookStrings.AbstractBaseModelStrings.
        created_at_verbose_name)
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=BookStrings.AbstractBaseModelStrings.
        updated_at_verbose_name)

    class Meta:
        abstract = True

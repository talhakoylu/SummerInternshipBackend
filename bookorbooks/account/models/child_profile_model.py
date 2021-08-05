from constants.account_strings import AccountStrings
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from country.models import City


class ChildProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=AccountStrings.ChildProfileStrings.user_verbose_name,
        related_name="user_child")
    city = models.ForeignKey(
        "country.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=AccountStrings.ChildProfileStrings.city_verbose_name,
        related_name="city_child_profiles")
    hobbies = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name=AccountStrings.ChildProfileStrings.hobbies_verbose_name)

    class Meta:
        verbose_name = AccountStrings.ChildProfileStrings.meta_verbose_name
        verbose_name_plural = AccountStrings.ChildProfileStrings.meta_verbose_name_plural

    @property
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return self.get_full_name

    def clean(self) -> None:
        """
        This method will check if the user type is a child during creation.
        """
        if self.user.user_type != 2:
            raise ValidationError(AccountStrings.ChildProfileStrings.user_type_error)

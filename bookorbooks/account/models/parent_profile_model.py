from django.core.exceptions import ValidationError
from constants.account_strings import AccountStrings
from django.db import models
from django.conf import settings
from country.models import City
from django.db.models.signals import post_delete
from django.dispatch import receiver

class ParentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=AccountStrings.ParentProfileStrings.user_verbose_name,
        related_name="user_parent")
    city = models.ForeignKey(
        "country.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=AccountStrings.ParentProfileStrings.city_verbose_name,
        related_name="city_parent_profiles")
    profession = models.CharField(max_length=500,
                                  null=True,
                                  blank=True,
                                  verbose_name=AccountStrings.
                                  ParentProfileStrings.profession_verbose_name)

    class Meta:
        verbose_name = AccountStrings.ParentProfileStrings.meta_verbose_name
        verbose_name_plural = AccountStrings.ParentProfileStrings.meta_verbose_name_plural

    @property
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return self.get_full_name

    def clean(self) -> None:
        """
        This method will check if the user type is a parent during creation.
        """
        if self.user.user_type != 3:
            raise ValidationError(AccountStrings.ParentProfileStrings.user_type_error)


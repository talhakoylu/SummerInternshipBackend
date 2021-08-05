from constants.account_strings import AccountStrings
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


class InstructorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=AccountStrings.InstructorProfileStrings.user_verbose_name,
        related_name="user_instructor")
    school = models.ForeignKey(
        "school.School",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=AccountStrings.InstructorProfileStrings.school_verbose_name,
        related_name="school_instructor")
    branch = models.CharField(
        max_length=50,
        verbose_name=AccountStrings.InstructorProfileStrings.branch_verbose_name)

    class Meta:
        verbose_name = AccountStrings.InstructorProfileStrings.meta_verbose_name
        verbose_name_plural = AccountStrings.InstructorProfileStrings.meta_verbose_name_plural

    @property
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return self.get_full_name

    def clean(self) -> None:
        """
        This method will check if the user type is an instructor.
        """
        if self.user.user_type != 4:
            raise ValidationError(AccountStrings.InstructorProfileStrings.user_type_error)

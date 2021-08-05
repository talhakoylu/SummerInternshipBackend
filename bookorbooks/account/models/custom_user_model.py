from account.models.instructor_model import InstructorProfile
from account.models.child_profile_model import ChildProfile
from account.models.parent_profile_model import ParentProfile
from constants.account_strings import AccountStrings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(UserManager):
    """
    Custom user model is inheriting from AbstractUser. For this reason, we haven't got responsibility 
    about writing CustomUserManager. However, username field has case sensetive. To solve this issue,
    <get_by_natural_key> method was overriden. 
    """
    def get_by_natural_key(self, username):
        """
        This is an overridden UserManager method. Initially, the username field is case sensitive.\n
        After applying this method, the username field becomes caseless.\n
        """
        case_insensitive_username_field = '{}__iexact'.format(
            self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        (1, AccountStrings.CustomUserStrings.gender_choice_male),
        (2, AccountStrings.CustomUserStrings.gender_choice_female),
        (3, AccountStrings.CustomUserStrings.gender_choice_other),
    )

    USER_TYPE_CHOICES = (
        (1, AccountStrings.CustomUserStrings.user_type_choice_default),
        (2, AccountStrings.CustomUserStrings.user_type_choice_child),
        (3, AccountStrings.CustomUserStrings.user_type_choice_parent),
        (4, AccountStrings.CustomUserStrings.user_type_choice_instructor),
    )
    objects = CustomUserManager()
    email = models.EmailField(max_length=255,
                              unique=True,
                              null=False,
                              blank=False)
    identity_number = models.CharField(
        max_length=11,
        unique=True,
        verbose_name=AccountStrings.CustomUserStrings.
        identity_number_verbose_name)
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=AccountStrings.CustomUserStrings.birth_date_verbose_name)
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES,
        default=1,
        verbose_name=_(AccountStrings.CustomUserStrings.gender_verbose_name))
    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES,
        default=1,
        verbose_name=AccountStrings.CustomUserStrings.user_type_verbose_name)

    class Meta:
        verbose_name = AccountStrings.CustomUserStrings.meta_verbose_name
        verbose_name_plural = AccountStrings.CustomUserStrings.meta_verbose_name_plural

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def change_user_type(self):
        """
        This method is responsible for creating extra fields according to the user type and deleting the old record when the user profile is updated.
        """
        user_origin = CustomUser.objects.get(id=self.id)
        if user_origin.user_type != self.user_type:
            ChildProfile.objects.filter(user=self).delete()
            ParentProfile.objects.filter(user=self).delete()
            InstructorProfile.objects.filter(user=self).delete()
            if user_origin.user_type == 1:
                if self.user_type == 2:
                    ChildProfile.objects.get_or_create(user=self)
                elif self.user_type == 3:
                    ParentProfile.objects.get_or_create(user=self)
                elif self.user_type == 4:
                    InstructorProfile.objects.get_or_create(user=self)
            elif user_origin.user_type == 2:
                if self.user_type == 3:
                    ParentProfile.objects.get_or_create(user=self)
                elif self.user_type == 4:
                    InstructorProfile.objects.get_or_create(user=self)
            elif user_origin.user_type == 3:
                if self.user_type == 2:
                    ChildProfile.objects.get_or_create(user=self)
                elif self.user_type == 4:
                    InstructorProfile.objects.get_or_create(user=self)
            elif user_origin.user_type == 4:
                if self.user_type == 2:
                    ChildProfile.objects.get_or_create(user=self)
                elif self.user_type == 3:
                    ParentProfile.objects.get_or_create(user=self)

    def save(self, *args, **kwargs):
        """
        This is an overridden save method of CustomUserModel. Through this method, 
        the user type is checked and the row is created in the profile table to which the user belongs.
        """
        if not self.id:
            super(CustomUser, self).save(*args, **kwargs)
            if self.user_type == 2:
                return ChildProfile.objects.create(user=self)
            elif self.user_type == 3:
                return ParentProfile.objects.create(user=self)
            elif self.user_type == 4:
                return InstructorProfile.objects.create(user=self)
        else:
            self.change_user_type()

        return super(CustomUser, self).save(*args, **kwargs)

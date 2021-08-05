from django.db import models
from constants.quiz_strings import QuizStrings


class AbstractQuizBaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=QuizStrings.AbstractBaseStrings.created_at_verbose_name)
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=QuizStrings.AbstractBaseStrings.updated_at_verbose_name)

    class Meta:
        abstract = True

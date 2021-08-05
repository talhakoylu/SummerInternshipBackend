from django.utils.functional import cached_property
from constants.quiz_strings import QuizStrings
from django.db import models
from quiz.models.abstract_base_model import AbstractQuizBaseModel
from django.utils.translation import ugettext_lazy as _


class Quiz(AbstractQuizBaseModel):
    ENABLED_CHOICES = (
        (True, _("Aktif")),
        (False, _("Aktif Değil")),
    )
    
    book = models.ForeignKey("book.Book", on_delete= models.CASCADE, related_name="book_quiz", verbose_name=QuizStrings.QuizStrings.book_verbose_name)
    title = models.CharField(max_length=150, verbose_name=QuizStrings.QuizStrings.title_verbose_name)
    enabled = models.BooleanField(choices=ENABLED_CHOICES,verbose_name=QuizStrings.QuizStrings.enabled_verbose_name, default=False)

    class Meta:
        verbose_name = QuizStrings.QuizStrings.meta_quiz_verbose_name
        verbose_name_plural = QuizStrings.QuizStrings.meta_quiz_verbose_name_plural

    def __str__(self):
        return f"{self.title} - \"{self.book.name}\""

    @cached_property
    def get_quiz_name_with_book_name(self):
        return f"{self.title} - {self.book.name}"

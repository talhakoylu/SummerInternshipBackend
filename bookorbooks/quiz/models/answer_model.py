from constants.quiz_strings import QuizStrings
from quiz.models.abstract_base_model import AbstractQuizBaseModel
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _


class Answer(AbstractQuizBaseModel):
    IS_CORRECT_CHOICES = (
        (True, _("Doğru Cevap")),
        (False, _("Yanlış Cevap"))
    )

    question = models.ForeignKey("quiz.Question", on_delete=models.CASCADE, related_name = "question_answer", verbose_name=QuizStrings.AnswerStrings.question_verbose_name)
    answer = models.CharField(max_length=500, verbose_name=QuizStrings.AnswerStrings.answer_verbose_name)
    is_correct = models.BooleanField(choices=IS_CORRECT_CHOICES, verbose_name=QuizStrings.AnswerStrings.is_correct_verbose_name, default=False)

    def __str__(self) -> str:
        return f"{self.answer}"

    @cached_property
    def answer_short(self):
        return f"{self.answer[:100]}"

    class Meta:
        verbose_name = QuizStrings.AnswerStrings.meta_answer_verbose_name
        verbose_name_plural = QuizStrings.AnswerStrings.meta_answer_verbose_name_plural
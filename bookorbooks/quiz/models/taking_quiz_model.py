from django.utils.functional import cached_property
from constants.quiz_strings import QuizStrings
from quiz.models.abstract_base_model import AbstractQuizBaseModel
from django.db import models

class TakingQuiz(AbstractQuizBaseModel):
    quiz = models.ForeignKey("quiz.Quiz", on_delete=models.DO_NOTHING, related_name="quiz_taking_quiz", verbose_name = QuizStrings.TakingQuizStrings.quiz_verbose_name)
    child = models.ForeignKey("account.ChildProfile", on_delete=models.CASCADE, related_name = "child_taking_quiz", verbose_name=QuizStrings.TakingQuizStrings.child_verbose_name)
    title = models.CharField(max_length=150, editable=False, default="-", verbose_name=QuizStrings.TakingQuizStrings.title_verbose_name)
    total_point = models.PositiveIntegerField(default=0, verbose_name=QuizStrings.TakingQuizStrings.total_point_verbose_name)

    class Meta:
        verbose_name = QuizStrings.TakingQuizStrings.meta_verbose_name
        verbose_name_plural = QuizStrings.TakingQuizStrings.meta_verbose_name_plural


    @cached_property
    def get_taking_quiz_title(self):
        return f"{self.child.user.first_name} {self.child.user.last_name} - {self.quiz.title}"

    def __str__(self) -> str:
        return self.get_taking_quiz_title

    def save(self, *args, **kwargs):
        """
        This is an overridden save method of TakingQuiz Model. Through this method, 
        the taking quiz title will be created automatically.
        """
        self.title = self.get_taking_quiz_title

        return super(TakingQuiz, self).save(*args, **kwargs)
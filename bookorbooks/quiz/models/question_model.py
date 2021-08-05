from constants.quiz_strings import QuizStrings
from quiz.models.abstract_base_model import AbstractQuizBaseModel
from django.db import models


class Question(AbstractQuizBaseModel):
    quiz = models.ForeignKey("quiz.Quiz", on_delete=models.DO_NOTHING, related_name="question_quiz", verbose_name=QuizStrings.QuestionStrings.quiz_verbose_name)
    question = models.CharField(max_length=500, verbose_name= QuizStrings.QuestionStrings.question_verbose_name)
    topic = models.CharField(max_length=500, verbose_name=QuizStrings.QuestionStrings.topic_verbose_name, help_text=QuizStrings.QuestionStrings.topic_hint_text)

    def __str__(self) -> str:
        return f"{self.question}"

    @property
    def question_short(self):
        return f"{self.question[:100]}"
    
    @property
    def topic_short(self):
        return f"{self.topic[:100]}"

    class Meta:
        verbose_name = QuizStrings.QuestionStrings.meta_question_verbose_name
        verbose_name_plural = QuizStrings.QuestionStrings.meta_question_verbose_name_plural
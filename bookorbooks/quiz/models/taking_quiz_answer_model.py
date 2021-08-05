from django.core.exceptions import ValidationError
from constants.quiz_strings import QuizStrings
from quiz.models.abstract_base_model import AbstractQuizBaseModel
from django.db import models

class TakingQuizAnswer(AbstractQuizBaseModel):
    taking_quiz = models.ForeignKey("quiz.TakingQuiz", on_delete=models.CASCADE, related_name="taking_quizes", verbose_name=QuizStrings.TakingQuizAnswersStrings.taking_quiz_verbose_name)
    question = models.ForeignKey("quiz.Question", on_delete=models.DO_NOTHING, related_name="question_taking_quiz", verbose_name=QuizStrings.TakingQuizAnswersStrings.question_verbose_name)
    answer = models.ForeignKey("quiz.Answer", on_delete= models.DO_NOTHING, related_name="answer_taking_quiz", verbose_name=QuizStrings.TakingQuizAnswersStrings.answer_verbose_name)
    taking_quiz_title = models.TextField(editable=False, null=True, blank=True, verbose_name=QuizStrings.TakingQuizAnswersStrings.taking_quiz_title_verbose_name)
    question_text = models.TextField(editable=False, null=True, blank=True, verbose_name=QuizStrings.TakingQuizAnswersStrings.question_verbose_name)
    question_topic_content = models.TextField(editable=False, null=True, blank=True, verbose_name=QuizStrings.TakingQuizAnswersStrings.question_topic_verbose_name)
    answer_text = models.TextField(editable=False, null=True, blank=True, verbose_name=QuizStrings.TakingQuizAnswersStrings.answer_verbose_name)
    answer_is_correct = models.BooleanField(editable=False, null=True, blank=True, verbose_name=QuizStrings.TakingQuizAnswersStrings.answer_is_correct_verbose_name)

    class Meta:
        verbose_name = QuizStrings.TakingQuizAnswersStrings.meta_verbose_name
        verbose_name_plural = QuizStrings.TakingQuizAnswersStrings.meta_verbose_name_plural

    def __str__(self) -> str:
        return f"{self.taking_quiz.title}"

    def save(self, *args, **kwargs):
        """
        This is an overridden save method of TakingQuiz Model. Through this method, 
        the taking quiz title will be created automatically.
        """
        self.taking_quiz_title = self.taking_quiz.get_taking_quiz_title
        self.question_text = self.question.question
        self.question_topic_content = self.question.topic
        self.answer_text = self.answer.answer
        self.answer_is_correct = self.answer.is_correct

        return super(TakingQuizAnswer, self).save(*args, **kwargs)
    
    def clean(self) -> None:
        """
        Checks that whether the question id and the answer id are equal, and also checks whether the selected question is belong to solved exam.
        """
        if self.question != self.answer.question:
                raise ValidationError("The selected answer must belong to the selected question.")
        if self.taking_quiz.quiz != self.question.quiz:
            raise ValidationError("The selected question must belong to the selected quiz.")
        
       

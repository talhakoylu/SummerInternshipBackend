from quiz.models.answer_model import Answer
from quiz.models.question_model import Question
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from quiz.models import Quiz


class QuizStandardSerializer(ModelSerializer):
    """
        Returns the quiz details with book name and quiz's full title attribute.
    """
    book_name = serializers.CharField(source="book")
    quiz_full_title = serializers.CharField(
        source="get_quiz_name_with_book_name")

    class Meta:
        model = Quiz
        fields = "__all__"

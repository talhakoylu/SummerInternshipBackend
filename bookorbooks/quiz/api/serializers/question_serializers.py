from quiz.models.answer_model import Answer
from quiz.models.quiz_model import Quiz
from rest_framework.serializers import ModelSerializer
from quiz.models import Question


class AnswerSerializer(ModelSerializer):
    """
        Helper serializer. Do not use in views, you can use only this serializers file.
    """
    class Meta:
        model = Answer
        fields = "__all__"


class QuestionSerializer(ModelSerializer):
    """
        Returns the question details with answers of that question.
    """
    answers = AnswerSerializer(many = True, source = "question_answer")
    class Meta:
        model = Question
        fields = "__all__"

class QuestionWithQuizSerializer(ModelSerializer):
    """
        This serializer is return the response with quiz details, list of quiz's questions and at the same time 
        the list of question's answers.
    """
    questions = QuestionSerializer(many = True, source = "question_quiz")
    
    class Meta:
        model = Quiz
        fields = "__all__"
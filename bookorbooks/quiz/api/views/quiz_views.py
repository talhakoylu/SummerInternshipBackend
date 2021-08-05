from quiz.api.serializers.quiz_serializers import QuizStandardSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from quiz.models import Quiz
from rest_framework.permissions import IsAuthenticated


class QuizListAllAPIView(ListAPIView):
    """
        Returns the list of all quizzes
    """

    queryset = Quiz.objects.all()
    serializer_class = QuizStandardSerializer
    permission_classes = [IsAuthenticated]

class OnlyEnabledQuizesAPIView(ListAPIView):
    """
        Returns the list of only enabled quizzes.
    """
    serializer_class = QuizStandardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(enabled = True)

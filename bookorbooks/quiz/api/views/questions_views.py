from quiz.models.question_model import Question
from django.shortcuts import get_list_or_404
from quiz.models.quiz_model import Quiz
from rest_framework.permissions import IsAuthenticated
from quiz.api.serializers.question_serializers import QuestionSerializer, QuestionWithQuizSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404


class GetQuestionsByQuizIdAPIView(RetrieveAPIView):
    """
        Returns a list of questions that belongs to the current quiz id.
    """
    serializer_class = QuestionWithQuizSerializer
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(Quiz, id=self.kwargs["quiz_id"])
        self.check_object_permissions(self.request, obj)
        return obj


class GetQuestionsByEnabledQuizIdAPIView(RetrieveAPIView):
    """
        Returns the list of last added enabled quiz's questions by quiz id.
    """
    serializer_class = QuestionWithQuizSerializer
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(Quiz, id=self.kwargs["quiz_id"], enabled = True)
        self.check_object_permissions(self.request, obj)
        return obj


class QuestionsAllAPIView(ListAPIView):
    """
        Returns the list of all questions.
    """
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()

class GetQuestionByIdAPIView(RetrieveAPIView):
    """
        Returns a specific question object by id value.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(Question, id=self.kwargs["id"])
        self.check_object_permissions(self.request, obj)
        return obj


class GetQuizByBookIdAPIView(ListAPIView):
    """
        Returns a specific quiz by book id.
    """
    serializer_class = QuestionWithQuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(book_id = self.kwargs["book_id"])

class GetLastEnabledQuizByBookIdAPIView(RetrieveAPIView):
    """
        Returns a specific quiz by book id.
    """
    serializer_class = QuestionWithQuizSerializer
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = Quiz.objects.filter(book_id = self.kwargs["book_id"], enabled = True).last()
        self.check_object_permissions(self.request, obj)
        return obj
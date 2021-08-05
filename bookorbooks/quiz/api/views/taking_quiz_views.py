from book.models.reading_history_model import ReadingHistory
from constants.quiz_strings import QuizStrings
from django.core.exceptions import ValidationError
from rest_framework import status
from quiz.models.question_model import Question
from quiz.models.answer_model import Answer
from account.models import instructor_model
from quiz.models.taking_quiz_answer_model import TakingQuizAnswer
from quiz.models.taking_quiz_model import TakingQuiz
from school.api.permissions import IsOwnClass
from school.models.class_model import Class
from account.models.instructor_model import InstructorProfile
from rest_framework.permissions import IsAuthenticated
from quiz.api.serializers.taking_quiz_serializers import TakingQuizAnswerCreateSerializer, TakingQuizCreateSerializer, TakingQuizDetailsForInstructorSerializer, TakingQuizDetailsForParentSerializer, TakingQuizDetailsForSpecificClassSerializer, TakingQuizSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, get_object_or_404
from account.models import ParentProfile
from account.api.permissions import IsChild, IsInstructor, IsParent
from rest_framework.response import Response


class TakingQuizHistoryByParentAPIView(RetrieveAPIView):
    """
        Returns a list of the quiz history of parent's children.
    """
    queryset = ParentProfile.objects.all()
    serializer_class = TakingQuizDetailsForParentSerializer
    permission_classes = [IsAuthenticated, IsParent]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(ParentProfile, user=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj


class TakingQuizHistoryByInstructorAPIView(RetrieveAPIView):
    """
        Returns a list of the instructor's class students' quiz history.
    """
    queryset = InstructorProfile.objects.all()
    serializer_class = TakingQuizDetailsForInstructorSerializer
    permission_classes = [IsAuthenticated, IsInstructor]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(InstructorProfile, user=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj


class StudentsTakingQuizHistoryByClassIdAPIView(RetrieveAPIView):
    """
        Returns the list of a specific class' students and their quiz results.
    """
    queryset = Class.objects.all()
    serializer_class = TakingQuizDetailsForSpecificClassSerializer
    permission_classes = [IsAuthenticated, IsInstructor, IsOwnClass]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(Class, id=self.kwargs["class_id"])
        self.check_object_permissions(self.request, obj)
        return obj


class TakingQuizListByChildAPIView(ListAPIView):
    """
        Returns the list of the requester child's quiz results.
    """
    serializer_class = TakingQuizSerializer
    permission_classes = [IsAuthenticated, IsChild]

    def get_queryset(self):
        return TakingQuiz.objects.filter(child=self.request.user.user_child)


class CreateTakingQuizAPIView(CreateAPIView):
    """
        An API View about to add a new TakingQuiz record.
    """
    queryset = TakingQuiz.objects.all()
    serializer_class = TakingQuizCreateSerializer
    permission_classes = [IsAuthenticated, IsChild]

    def perform_create(self, serializer):
        return serializer.save(child=self.request.user.user_child)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = serializer.validated_data.get("quiz",)
        obj = ReadingHistory.objects.filter(child = request.user.user_child, book = quiz.book, is_finished = True)
        if not obj.exists():
            return Response({"error": QuizStrings.ValidationErrorMessages.reading_must_finished}, status=status.HTTP_403_FORBIDDEN)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)


class UpdateTakingQuizAPIView(RetrieveUpdateAPIView):
    """
        An API View about to update the an existing TakingQuiz record.
    """
    queryset = TakingQuiz.objects.all()
    serializer_class = TakingQuizCreateSerializer
    permission_classes = [IsAuthenticated, IsChild]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(TakingQuiz, child_id = self.request.user.id, id = self.kwargs["id"])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        return serializer.save(child=self.request.user.user_child)


class CreateTakingQuizAnswerAPIView(CreateAPIView):
    """
        An API View for adding a data to TakingQuizAnswer table. Create method of this class has been overridden about to validation.
    """
    queryset = TakingQuizAnswer.objects.all()
    serializer_class = TakingQuizAnswerCreateSerializer
    permission_classes = [IsAuthenticated, IsChild]

    def create(self, request, *args, **kwargs):
        """
            It is an overridden method to check whether the question in the sent request belongs to the relevant exam and whether the answer given belongs to that question.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        taking_quiz = serializer.validated_data.get("taking_quiz",)
        answer = serializer.validated_data.get("answer",)
        question = serializer.validated_data.get("question",)

        if taking_quiz.quiz != answer.question.quiz:
            return Response({"error": QuizStrings.ValidationErrorMessages.answer_is_not_belong_to_question}, status=status.HTTP_403_FORBIDDEN)
        elif answer.question != question:
            return Response({"error": QuizStrings.ValidationErrorMessages.question_is_not_belong_to_quiz}, status=status.HTTP_403_FORBIDDEN)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
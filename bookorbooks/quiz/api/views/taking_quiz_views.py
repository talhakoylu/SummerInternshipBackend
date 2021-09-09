from datetime import datetime
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
from django.shortcuts import get_list_or_404
from book.models.reading_history_model import ReadingHistory
from constants.quiz_strings import QuizStrings
from rest_framework import status
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
        obj = InstructorProfile.objects.filter(user=self.request.user.id)
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


class TakingQuizListByChildIdAPIView(ListAPIView):
    """
        Returns the list of the requester child's quiz results.
    """
    serializer_class = TakingQuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TakingQuiz.objects.filter(child=self.kwargs["child_id"])


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
        quiz = serializer.validated_data.get("quiz", )
        obj = ReadingHistory.objects.filter(child=request.user.user_child,
                                            book=quiz.book,
                                            is_finished=True)
        if not obj.exists():
            return Response(
                {
                    "error":
                    QuizStrings.ValidationErrorMessages.reading_must_finished
                },
                status=status.HTTP_403_FORBIDDEN)
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
        obj = get_object_or_404(TakingQuiz,
                                child_id=self.request.user.id,
                                id=self.kwargs["id"])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        # return serializer.save(child=self.request.user.user_child)
        data = TakingQuizAnswer.objects.filter(
            taking_quiz_id=self.kwargs["id"]).aggregate(
                answer_count=Count('question', distinct=True),
                wrong_count=Count('answer_is_correct',
                                  filter=Q(answer_is_correct=False)))
        if data['answer_count'] == 0:
            question_point = 0
            total_point = 0
        else:
            question_point = 100 / data['answer_count']
            total_point = 100 - (question_point * data['wrong_count'])

        if data == None or data['answer_count'] == None or data[
                'wrong_count'] == None or total_point == None or question_point == None:
            return serializer.save(child=self.request.user.user_child,
                                   total_point=0)
        elif total_point < 0:
            return serializer.save(child=self.request.user.user_child,
                                   total_point=0)
        elif total_point > 100:
            return serializer.save(child=self.request.user.user_child,
                                   total_point=100)
        else:
            return serializer.save(child=self.request.user.user_child,
                                   total_point=total_point)


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
        taking_quiz = serializer.validated_data.get("taking_quiz", )
        answer = serializer.validated_data.get("answer", )
        question = serializer.validated_data.get("question", )

        if taking_quiz.quiz != answer.question.quiz:
            return Response(
                {"error": QuizStrings.ValidationErrorMessages.answer_is_not_belong_to_question}, status=status.HTTP_403_FORBIDDEN)
        elif answer.question != question:
            return Response({"error": QuizStrings.ValidationErrorMessages.question_is_not_belong_to_quiz}, status=status.HTTP_403_FORBIDDEN)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        This is an overridden perform_create method. The main purpose of this process is if the user replies to a question they have already answered, they update the existing record instead of creating a new record.
        """
        taking_quiz = serializer.validated_data.get('taking_quiz', )
        question = serializer.validated_data.get('question', )
        answer = serializer.validated_data.get('answer', )
        obj_lst = TakingQuizAnswer.objects.filter(taking_quiz=taking_quiz,
                                                  question=question)
        if obj_lst:
            answer_text = answer.answer
            answer_is_correct = answer.is_correct
            return obj_lst.update(answer=answer, answer_text = answer_text, answer_is_correct = answer_is_correct, updated_at=datetime.now())
        else:
            return TakingQuizAnswer.objects.create(taking_quiz=taking_quiz,
                                                   question=question,
                                                   answer=answer)

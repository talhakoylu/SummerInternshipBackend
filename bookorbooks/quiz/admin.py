from quiz.models.taking_quiz_answer_model import TakingQuizAnswer
from quiz.models.taking_quiz_model import TakingQuiz
from quiz.models.answer_model import Answer
from quiz.models.question_model import Question
from django.contrib import admin
from quiz.models import Quiz
from django import forms
from constants.quiz_strings import QuizStrings


class QuestionAdminForm(forms.ModelForm):
    """
    This class is overrides question  and topic fields. In this way, user sees a textfield area
    instead of charfield area in admin page.
    """
    class Meta:
        model = Question
        fields = "__all__"
        widgets = {
            "question": forms.Textarea(attrs={
                'cols': 80,
                'rows': 3
            }),
            "topic": forms.Textarea(attrs={
                'cols': 80,
                'rows': 10
            })
        }


class AnswerAdminForm(forms.ModelForm):
    """
    This class is overrides the answer field. In this way, user sees a textfield area
    instead of charfield area in admin page.
    """
    class Meta:
        model = Answer
        fields = "__all__"
        widgets = {
            "answer": forms.Textarea(attrs={
                'cols': 80,
                'rows': 4
            })
        }


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ["id", "__str__", "book", "enabled","created_at", "updated_at"]
    list_display_links = ["id", "__str__"]
    search_fields = [ "book__name", "title"]
    autocomplete_fields = ["book"]
    class Meta:
        model = Quiz


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ["id", "question_short", "quiz", "topic_short","created_at", "updated_at"]
    list_display_links = ["id", "question_short"]
    search_fields = ["question", "quiz__title", "quiz__book__name", "topic"]
    autocomplete_fields = ["quiz"]

    class Meta:
        model = Question

    def question_short(self, obj):
        return obj.question_short
    question_short.admin_order_field  = 'question'  
    question_short.short_description = QuizStrings.QuestionStrings.question_verbose_name

    def topic_short(self, obj):
        return obj.topic_short
    topic_short.admin_order_field  = 'topic'  
    topic_short.short_description = QuizStrings.QuestionStrings.topic_verbose_name

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    form = AnswerAdminForm
    list_display = ("id", "answer_short", "question_short", "quiz_title", "is_correct", "created_at", "updated_at")
    list_display_links = ["id", "answer_short"]
    search_fields = ["answer", "question__question", "question__quiz__title", "question__quiz__book__name"]
    autocomplete_fields = ["question"]

    class Meta:
        model = Answer

    def quiz_title(self, obj):
        return obj.question.quiz.title
    quiz_title.admin_order_field  = 'question__quiz_id'  
    quiz_title.short_description = QuizStrings.QuizStrings.meta_quiz_verbose_name
    
    
    def answer_short(self, obj):
        return obj.answer_short
    answer_short.admin_order_field  = 'answer'  
    answer_short.short_description = QuizStrings.AnswerStrings.answer_verbose_name
    
    
    def question_short(self, obj):
        return obj.question.question_short
    question_short.admin_order_field  = 'question'  
    question_short.short_description = QuizStrings.QuestionStrings.question_verbose_name

@admin.register(TakingQuiz)
class TakingQuizAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "get_quiz_title", "get_quiz_book", "child", "total_point","created_at", "updated_at"]
    list_display_links = ["id", "title"]
    search_fields = [ "id", "title", "quiz__title", "quiz__book__name", "child__user__first_name", "child__user__last_name"]
    autocomplete_fields = ["quiz"]
    exclude = ("title",)
    readonly_fields=('title', )
    class Meta:
        model = TakingQuiz

    def get_quiz_title(self, obj):
        return obj.quiz.title
    get_quiz_title.admin_order_field  = 'quiz__title'  
    get_quiz_title.short_description = QuizStrings.TakingQuizStrings.quiz_verbose_name
    
    def get_quiz_book(self, obj):
        return obj.quiz.book
    get_quiz_book.admin_order_field  = 'quiz__book__name'  
    get_quiz_book.short_description = QuizStrings.QuizStrings.book_verbose_name

@admin.register(TakingQuizAnswer)
class TakingQuizAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "taking_quiz_title", "question", "answer"]
    list_display_links = ["id", "taking_quiz_title"]
    search_fields = [ "id", "taking_quiz_title", "question_text", "question_topic_content", "answer_text", "taking_quiz__quiz__title", "taking_quiz__quiz__book"]
    autocomplete_fields = ["taking_quiz"]
    exclude = ("taking_quiz_title", "question_text", "question_topic_content", "answer_text", "answer_is_correct",)
    readonly_fields=("taking_quiz_title", "question_text", "question_topic_content", "answer_text", "answer_is_correct", )
    class Meta:
        model = TakingQuizAnswer
from quiz.api.views.taking_quiz_views import CreateTakingQuizAPIView, CreateTakingQuizAnswerAPIView, StudentsTakingQuizHistoryByClassIdAPIView, TakingQuizHistoryByInstructorAPIView, TakingQuizHistoryByParentAPIView, TakingQuizListByChildAPIView, UpdateTakingQuizAPIView
from quiz.api.views.questions_views import GetLastEnabledQuizByBookIdAPIView, GetQuestionByIdAPIView, GetQuestionsByEnabledQuizIdAPIView, GetQuestionsByQuizIdAPIView, QuestionsAllAPIView
from quiz.api.views.quiz_views import OnlyEnabledQuizesAPIView, QuizListAllAPIView
from django.urls import path

app_name = "quiz"

urlpatterns = [
    path("quiz-list-all", QuizListAllAPIView.as_view(), name="quiz_list_all"),
    path("enabled-quiz-list-all", OnlyEnabledQuizesAPIView.as_view(), name="enabled_quiz_list_all"),

    path("get-questions-by-quiz-id/<quiz_id>", GetQuestionsByQuizIdAPIView.as_view(), name="get_questions_by_quiz_id"),
    path("get-questions-by-enabled-quiz-id/<quiz_id>", GetQuestionsByEnabledQuizIdAPIView.as_view(), name="get_questions_by_enabled_quiz_id"),
    path("get-question-by-id/<id>", GetQuestionByIdAPIView.as_view(), name="get_question_by_id"),

    path("get-last-enabled-quiz-by-book-id/<book_id>", GetLastEnabledQuizByBookIdAPIView.as_view(), name = "get_last_enabled_quiz_by_book_id"),

    path("get-children-quiz-history", TakingQuizHistoryByParentAPIView.as_view(), name="get_children_quiz_history"),
    path("get-students-quiz-history", TakingQuizHistoryByInstructorAPIView.as_view(), name="get_students_quiz_history"),
    path("get-students-quiz-history-by-class/<class_id>", StudentsTakingQuizHistoryByClassIdAPIView.as_view(), name="get_students_quiz_history_by_class"),
    path("get-quiz-history-by-child", TakingQuizListByChildAPIView.as_view(), name="get_quiz_history_by_child"),
    path("create-taking-quiz", CreateTakingQuizAPIView.as_view(), name="create_taking_quiz"),
    path("update-taking-quiz/<id>", UpdateTakingQuizAPIView.as_view(), name="update_taking_quiz"),
    path("create-taking-quiz-answer", CreateTakingQuizAnswerAPIView.as_view(), name="create_taking_quiz_answer"),
]

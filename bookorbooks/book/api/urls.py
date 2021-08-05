from book.api.views.reading_history_views import AddReadingHistoryAPIView, ReadingHistoryByChildAPIView, ReadingHistoryByChildIdAPIView, ReadingHistoryListAllAPIView
from book.api.views import AuthorDetailAPIView, AuthorListAPIView, BookDetailAPIView, BookLanguageListAPIView, BookLevelListAPIView, BookListAPIView, BooksPageListAPIView, CategoryListAPIView, CategoryDetailAPIView, CategoryDetailWithBooksAPIView
from django.urls import path

app_name = "book"

urlpatterns = [
    path("category-list", CategoryListAPIView.as_view(), name="category-list"),
    path("category-detail/<slug>", CategoryDetailAPIView.as_view(), name="category-detail"),
    path("category-detail-with-books/<slug>", CategoryDetailWithBooksAPIView.as_view(), name="category-detail-with-books"),
    path("book-level-list", BookLevelListAPIView.as_view(), name="book-level-list"),
    path("book-language-list", BookLanguageListAPIView.as_view(), name="book-language-list"),
    path("author-list", AuthorListAPIView.as_view(), name="author-list"),
    path("author-detail/<slug>", AuthorDetailAPIView.as_view(), name="author-detail"),
    path("book-list", BookListAPIView.as_view(), name="book-list"),
    path("book-detail/<slug>", BookDetailAPIView.as_view(), name="book-detail"),
    path("books-page-list", BooksPageListAPIView.as_view(), name="books-page-list"),
    path("reading-history-list", ReadingHistoryListAllAPIView.as_view(), name="reading_history_list"),
    path("reading-history-list-by-child", ReadingHistoryByChildAPIView.as_view(), name="reading_history_list_by_child"),
    path("reading-history-list/<child_id>", ReadingHistoryByChildIdAPIView.as_view(), name="reading_history_list_by_child_id"),
    path("add-reading-history-record", AddReadingHistoryAPIView.as_view(), name="reading_history_add"),

]

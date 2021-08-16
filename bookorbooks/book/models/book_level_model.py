from book.models.abstract_book_base_model import AbstractBookBaseModel
from django.db import models
from constants.book_strings import BookStrings


class BookLevel(AbstractBookBaseModel):
    title = models.CharField(
        max_length=50,
        verbose_name=BookStrings.BookLevelStrings.title_verbose_name)
    title_english = models.CharField(
        max_length=50,
        verbose_name=BookStrings.BookLevelStrings.english_title_verbose_name)

    class Meta:
        verbose_name = BookStrings.BookLevelStrings.meta_verbose_name
        verbose_name_plural = BookStrings.BookLevelStrings.meta_verbose_name_plural

    def __str__(self):
        return self.title

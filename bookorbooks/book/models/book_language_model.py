from book.models.abstract_book_base_model import AbstractBookBaseModel
from django.db import models
from constants.book_strings import BookStrings


class BookLanguage(AbstractBookBaseModel):
    language_name = models.CharField(
        max_length=50,
        verbose_name=BookStrings.BookLanguageStrings.language_name_verbose_name
    )
    language_code = models.CharField(
        max_length=10,
        verbose_name=BookStrings.BookLanguageStrings.language_code_verbose_name
    )

    class Meta:
        verbose_name = BookStrings.BookLanguageStrings.meta_verbose_name
        verbose_name_plural = BookStrings.BookLanguageStrings.meta_verbose_name_plural

    def __str__(self):
        return self.language_name

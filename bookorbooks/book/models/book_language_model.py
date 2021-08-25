from book.models.abstract_book_base_model import AbstractBookBaseModel
from django.db import models
from constants.book_strings import BookStrings
from django.utils.functional import lazy
from django.utils.safestring import mark_safe

mark_safe_lazy = lazy(mark_safe, str)

class BookLanguage(AbstractBookBaseModel):
    language_name = models.CharField(
        max_length=50,
        verbose_name=BookStrings.BookLanguageStrings.language_name_verbose_name
    )
    language_code = models.CharField(
        max_length=10,
        verbose_name=BookStrings.BookLanguageStrings.language_code_verbose_name,
        help_text= mark_safe_lazy(BookStrings.BookLanguageStrings.language_code_help_text)
    )

    class Meta:
        verbose_name = BookStrings.BookLanguageStrings.meta_verbose_name
        verbose_name_plural = BookStrings.BookLanguageStrings.meta_verbose_name_plural

    def __str__(self):
        return self.language_name

from book.models.abstract_book_base_model import AbstractBookBaseModel
from django.db import models
from constants.book_strings import BookStrings
from django.utils.text import slugify


class ReadingHistory(AbstractBookBaseModel):
    IS_FINISHED = ((False,
                    BookStrings.ReadingHistoryStrings.is_finished_false),
                   (True, BookStrings.ReadingHistoryStrings.is_finished_true))
    book = models.ForeignKey(
        "book.Book",
        on_delete=models.CASCADE,
        related_name="book_reading_history",
        verbose_name=BookStrings.ReadingHistoryStrings.book_verbose_name)
    child = models.ForeignKey(
        "account.ChildProfile",
        on_delete=models.CASCADE,
        related_name="child_reading_history",
        verbose_name=BookStrings.ReadingHistoryStrings.child_verbose_name)
    is_finished = models.BooleanField(
        choices=IS_FINISHED,
        verbose_name=BookStrings.ReadingHistoryStrings.is_finished_verbose_name
    )
    counter = models.PositiveIntegerField(
        verbose_name=BookStrings.ReadingHistoryStrings.counter_verbose_name,
        editable=False, default=0)

    class Meta:
        verbose_name = BookStrings.ReadingHistoryStrings.meta_verbose_name
        verbose_name_plural = BookStrings.ReadingHistoryStrings.meta_verbose_name_plural

    def __str__(self):
        return f"{self.child.user.first_name} {self.child.user.last_name} - \"{self.book.name}\" "

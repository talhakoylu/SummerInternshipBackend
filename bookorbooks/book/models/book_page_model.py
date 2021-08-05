from book.models.abstract_book_base_model import AbstractBookBaseModel
from django.db import models
from constants.book_strings import BookStrings
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _


class BookPage(AbstractBookBaseModel):
    POSITION_CHOICES = (
        (0, _("Orta")),
        (1, _("Üst")),
        (2, _("Alt")),
    )


    book = models.ForeignKey(
        "book.Book",
        on_delete=models.CASCADE,
        verbose_name=BookStrings.BookPageStrings.book_verbose_name,
        related_name="book_pages")
    title = models.CharField(max_length=150, editable=False)
    content = models.TextField(
        verbose_name=BookStrings.BookPageStrings.content_verbose_name)
    page_number = models.PositiveIntegerField(
        verbose_name=BookStrings.BookPageStrings.page_number_verbose_name,
        null=True,
        blank=True)
    image = models.ImageField(
        upload_to="books/book-pages/%Y/%m/%d/",
        blank=True,
        null=True,
        verbose_name=BookStrings.BookPageStrings.image_verbose_name)
    image_position = models.SmallIntegerField(
        verbose_name=BookStrings.BookPageStrings.image_position_verbose_name,
        null=True,
        blank=True,
        choices=POSITION_CHOICES,
        default= 0,
        validators=[MinValueValidator(0),
                    MaxValueValidator(2)])
    content_position = models.SmallIntegerField(
        verbose_name=BookStrings.BookPageStrings.content_position_verbose_name,
        null=True,
        blank=True,
        choices=POSITION_CHOICES,
        default= 0,
        validators=[MinValueValidator(0),
                    MaxValueValidator(2)])

    @property
    def get_page_title(self):
        """
        This method creates a page title with the book name and page number. This title will be created automatically.
        """
        return "Book: {} Page: {}".format(self.book.name, self.page_number)

    def __str__(self):
        return self.get_page_title

    class Meta:
        verbose_name = BookStrings.BookPageStrings.meta_verbose_name
        verbose_name_plural = BookStrings.BookPageStrings.meta_verbose_name_plural

    def save(self, *args, **kwargs):
        """
        It's an overridden save method. In this way, the page title creates automatically.
        """
        self.title = self.get_page_title
        return super(BookPage, self).save(*args, **kwargs)

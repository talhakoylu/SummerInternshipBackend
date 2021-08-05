from book.models.abstract_book_base_model import AbstractBookBaseModel
from django.db import models
from constants.book_strings import BookStrings
from django.utils.text import slugify

class Book(AbstractBookBaseModel):
    category = models.ForeignKey(
        "book.Category",
        on_delete=models.DO_NOTHING,
        related_name="category_books",
        verbose_name=BookStrings.BookStrings.category_verbose_name)
    level = models.ForeignKey(
        "book.BookLevel",
        on_delete=models.DO_NOTHING,
        related_name="level_books",
        verbose_name=BookStrings.BookStrings.level_verbose_name)
    language = models.ForeignKey(
        "book.BookLanguage",
        on_delete=models.DO_NOTHING,
        related_name="language_books",
        verbose_name=BookStrings.BookStrings.language_verbose_name)
    name = models.CharField(
        max_length=150, verbose_name=BookStrings.BookStrings.name_verbose_name)
    description = models.TextField(
        verbose_name=BookStrings.BookStrings.description_verbose_name)
    cover_image = models.ImageField(
        upload_to="books/book-covers/%Y/%m/%d/",
        blank=True,
        null=True,
        verbose_name=BookStrings.BookStrings.cover_image_verbose_name)
    author = models.ForeignKey(
        "book.Author",
        on_delete=models.DO_NOTHING,
        verbose_name=BookStrings.BookStrings.author_verbose_name,
        related_name="books")
    page = models.PositiveIntegerField(
        verbose_name=BookStrings.BookStrings.page_verbose_name, default = 0, blank=True)
    slug = models.SlugField(unique=True, max_length=150, editable=False)

    class Meta:
        verbose_name = BookStrings.BookStrings.meta_verbose_name
        verbose_name_plural = BookStrings.BookStrings.meta_verbose_name_plural

    def __str__(self):
        return self.name

    def get_slug(self):
        """
        This method is providing a unique slug value for the Book model.\n
        Slug will be created from book's name
        """
        slug = slugify(self.name.replace("ı", "i"))
        unique = slug
        number = 1
        while Book.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1
        return unique

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self.get_slug()
        else:
            origin_obj = Book.objects.get(pk=self.pk)
            if origin_obj.name != self.name:
                self.slug = self.get_slug()
        return super(Book, self).save(*args, **kwargs)

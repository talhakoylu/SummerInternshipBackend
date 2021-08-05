from book.models.abstract_book_base_model import AbstractBookBaseModel
from django.db import models
from constants.book_strings import BookStrings
from django.utils.text import slugify


class Author(AbstractBookBaseModel):
    first_name = models.CharField(
        max_length=50, verbose_name=BookStrings.Author.first_name_verbose_name)
    last_name = models.CharField(
        max_length=50, verbose_name=BookStrings.Author.last_name_verbose_name)
    photo = models.ImageField(
        upload_to="books/authors/%Y/%m/%d/",
        blank=True,
        null=True,
        verbose_name=BookStrings.Author.photo_verbose_name)
    biography = models.TextField(
        verbose_name=BookStrings.Author.biography_verbose_name)
    slug = models.SlugField(unique=True, max_length=150, editable=False)

    class Meta:
        verbose_name = BookStrings.Author.meta_verbose_name
        verbose_name_plural = BookStrings.Author.meta_verbose_name_plural

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.get_full_name()

    def get_slug(self):
        """
        This method is providing a unique slug value for the Author model.\n
        Slug will be created from author's first and last name
        """
        slug = slugify(self.get_full_name().replace("ı", "i"))
        unique = slug
        number = 1
        while Author.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1
        return unique

    def save(self, *args, **kwargs):
        """
        It's an overriden save method. The slug value is checked before the data goes to the database.
        If the value is not unique, a unique slug value is generated.
        """
        if not self.id:
            self.slug = self.get_slug()
        else:
            origin_obj = Author.objects.get(pk=self.pk)
            origin_full_name = self.get_full_name(origin_obj)
            if origin_full_name != self.get_full_name():
                self.slug = self.get_slug()
        return super(Author, self).save(*args, **kwargs)

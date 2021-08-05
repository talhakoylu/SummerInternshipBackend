from book.models.abstract_book_base_model import AbstractBookBaseModel
from django.db import models
from constants.book_strings import BookStrings
from django.utils.text import slugify

class Category(AbstractBookBaseModel):
    title = models.CharField(
        max_length=50,
        verbose_name=BookStrings.CategoryStrings.title_verbose_name)
    description = models.CharField(
        max_length=256,
        verbose_name=BookStrings.CategoryStrings.description_verbose_name)
    slug = models.SlugField(unique=True, max_length=150, editable=False)

    class Meta:
        verbose_name = BookStrings.CategoryStrings.meta_verbose_name
        verbose_name_plural = BookStrings.CategoryStrings.meta_verbose_name_plural

    def __str__(self):
        return self.title

    def get_slug(self):
        """
        This method is providing a unique slug value for the Category model.
        """
        slug = slugify(self.title.replace("ı", "i"))
        unique = slug
        number = 1
        while Category.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1
        return unique

    def save(self, *args, **kwargs):
        """
        This is an overridden save method. The main purpose of this method is to detect whether the slug value is unqiue before the data goes to the database.
        If the slug value is not unique, then the get_slug method is called and created a unique slug value.
        """
        if not self.id:
            self.slug = self.get_slug()
        else:
            origin_obj = Category.objects.get(pk=self.pk)
            if origin_obj.title != self.title:
                self.slug = self.get_slug()
        return super(Category, self).save(*args, **kwargs)

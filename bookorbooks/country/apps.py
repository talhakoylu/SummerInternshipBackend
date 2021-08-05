from constants.country_strings import CountryStrings
from django.apps import AppConfig


class CountryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'country'
    verbose_name = CountryStrings.CountryStrings.app_verbose_name

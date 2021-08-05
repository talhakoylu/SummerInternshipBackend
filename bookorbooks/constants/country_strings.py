from django.utils.translation import ugettext_lazy as _

class CountryStrings():
    class CountryStrings():
        meta_verbose_name = _("Ülke")
        meta_verbose_name_plural = _("Ülkeler")
        name_verbose_name = _("Ülke")
        code_verbose_name = _("Ülke Kodu")
        app_verbose_name = _("Ülke")
    
    class CityStrings():
        country_verbose_name = _("Ülke")
        meta_verbose_name = _("Şehir")
        meta_verbose_name_plural = _("Şehirler")
        name_verbose_name = _("Şehir")
        code_verbose_name = _("Şehir Kodu")
    
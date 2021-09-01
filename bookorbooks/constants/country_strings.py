from django.utils.translation import ugettext_lazy as _

class CountryStrings():
    class CountryStrings():
        meta_verbose_name = _("ülke")
        meta_verbose_name_plural = _("ülkeler")
        name_verbose_name = _("Ülke")
        code_verbose_name = _("Ülke Kodu")
        app_verbose_name = _("Ülke")
    
    class CityStrings():
        country_verbose_name = _("Ülke")
        district_verbose_name = _("Bölge")
        meta_verbose_name = _("şehir")
        meta_verbose_name_plural = _("şehirler")
        name_verbose_name = _("Şehir")
        code_verbose_name = _("Şehir Kodu")
        country_validation_error = _("In order to add this city, the country and district information must be linked.")


    class DistrictStrings():
        country_verbose_name = _("Ülke")
        meta_verbose_name = _("bölge")
        meta_verbose_name_plural = _("bölgeler")
        name_verbose_name = _("Bölge")
    
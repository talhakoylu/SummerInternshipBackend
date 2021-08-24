from django.utils.translation import ugettext_lazy as _

class SchoolStrings():
    class SchoolStrings():
        city_verbose_name = _("Şehirler")
        name_verbose_name = _("Okul Adı")
        address_verbose_name = _("Adres")
        website_verbose_name = _("Web Adresi")
        meta_verbose_name = _("Okul")
        meta_verbose_name_plural = _("Okullar")
    
    class ClassStrings():
        school_verbose_name = _("Okul")
        instructor_verbose_name = _("Eğitmen")
        name_verbose_name = _("Sınıf Adı")
        grade_verbose_name = _("Sınıf Derecesi")
        meta_verbose_name = _("Sınıf")
        meta_verbose_name_plural = _("Sınıflar")
        instructor_not_working_at_this_school_error = _("You cannot assign this instructor to a class from this school. The instructor does not work in this school.")
    
    class StudentListStrings():
        school_class_verbose_name = _("Sınıf")
        child_verbose_name = _("Öğrenci/Çocuk")
        meta_verbose_name = _("Sınıf Öğrencisi")
        meta_verbose_name_plural = _("Sınıf Öğrencileri")
        child_already_added_to_this_class_error = _("Because this student was previously added to this class, you cannot add them again.")
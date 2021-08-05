from django.utils.translation import ugettext_lazy as _

class AccountStrings():
    class CustomUserStrings():
        gender_choice_male = _("Erkek")
        gender_choice_female = _("Kadın")
        gender_choice_other = _("Other")
        user_type_choice_child = _("Çocuk")
        user_type_choice_parent = _("Ebeveyn")
        user_type_choice_instructor = _("Eğitmen")
        user_type_choice_default = _("Default")
        user_type_choice_admin = _("Yönetici")
        identity_number_verbose_name = _("Kimlik Numarası")
        birth_date_verbose_name = _("Doğum Tarihi")
        gender_verbose_name = _("Cinsiyet")
        user_type_verbose_name = _("Hesap Türü")
        meta_verbose_name = _("Kullanıcı")
        meta_verbose_name_plural = _("Kullanıcılar")

    class ChildProfileStrings():
        user_verbose_name = _("Kullanıcı")
        city_verbose_name = _("Şehir")
        hobbies_verbose_name = _("Hobiler")
        meta_verbose_name = _("Çocuk")
        meta_verbose_name_plural = _("Çocuklar")
        user_type_error = _("Kullanıcı bir çocuk olarak belirtilmemiş, ekleyebilmek için önce hesap ayarlarından statüsünü çocuk yapın!")
    
    class ParentProfileStrings():
        user_verbose_name = _("Kullanıcı")
        city_verbose_name = _("Şehir")
        profession_verbose_name = _("Meslek")
        meta_verbose_name = _("Ebeveyn")
        meta_verbose_name_plural = _("Ebeveynler")
        user_type_error = _("Kullanıcı bir ebevyn olarak belirtilmemiş, ekleyebilmek için önce hesap ayarlarından statüsünü ebeveyn yapın!")
    
    
    class InstructorProfileStrings():
        user_verbose_name = _("Kullanıcı")
        school_verbose_name = _("Okul")
        branch_verbose_name = _("Branş")
        meta_verbose_name = _("Eğitmen")
        meta_verbose_name_plural = _("Eğitmenler")
        user_type_error = _("Kullanıcı bir eğitmen olarak belirtilmemiş, ekleyebilmek için önce hesap ayarlarından statüsünü eğitmen yapın!")

    class ChildListString():
        parent_verbose_name = _("Ebeveyn")
        child_verbose_name = _("Çocuk")
        meta_verbose_name = _("Ebeveyn ve Çocuk Kaydı")
        meta_verbose_name_plural = _("Ebeveyn ve Çocuk Kayıtları")

    class RegisterSerializerStrings():
        user_type_error = _("You cannot pass data other than: 1- default, 2- child, 3- parent, 4- instructor")
        gender_error = _("You cannot pass data other than: 1- male, 2- female, 3- other")
        identity_number_error = _("Identity number can only consist of numbers and cannot be long than 11.")

    class PermissionStrings():
        is_parent_message = _("To do this, you must be a parent.")
        is_child_message = _("To do this, you must be a child.")
        is_instructor_message = _("To do this, you must be a instructor.")
        is_instructor_has_school_message = _("To do this, you have to choose the school you work at from your profile page. If the problem persists, please contact the administrator.")
        is_own_class_message = _("To do this, you must be the owner of this class.")
        is_own_child_message = _("To do this, you must be the parent of this child.")
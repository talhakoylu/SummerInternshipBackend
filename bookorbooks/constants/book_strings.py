from django.utils.translation import ugettext_lazy as _

class BookStrings():
    class BookLanguageStrings():
        meta_verbose_name = _("Dil")
        meta_verbose_name_plural = _("Diller")
        language_name_verbose_name = _("Dil")
        language_code_verbose_name = _("Dil Kodu")

    class AbstractBaseModelStrings():
        created_at_verbose_name = _("Oluşturulma Tarihi")
        updated_at_verbose_name = _("Güncellenme Tarihi")

    class CategoryStrings():
        title_verbose_name = _("Türkçe Başlık")
        english_title_verbose_name = _("İngilizce Başlık")
        description_verbose_name = _("Türkçe Açıklama")
        english_description_verbose_name = _("İngilizce Açıklama")
        meta_verbose_name = _("Kategori")
        meta_verbose_name_plural = _("Kategoriler")

    class BookLevelStrings():
        title_verbose_name = _("Başlık")
        english_title_verbose_name = _("İngilizce Başlık")
        meta_verbose_name = _("Seviye")
        meta_verbose_name_plural = _("Kitap Seviyeleri")

    class BookStrings():
        category_verbose_name = _("Kategori")
        level_verbose_name = _("Seviye")
        language_verbose_name = _("Kitap Dili")
        name_verbose_name = _("İsim")
        description_verbose_name = _("Açıklama")
        author_verbose_name = _("Yazar")
        page_verbose_name = _("Sayfa Sayısı")
        cover_image_verbose_name = _("Kapak Görseli")
        meta_verbose_name = _("Kitap")
        meta_verbose_name_plural = _("Kitaplar")

    class Author():
        first_name_verbose_name = _("İsim")
        last_name_verbose_name = _("Soyisim")
        photo_verbose_name = _("Fotoğraf")
        biography_verbose_name = _("Biyografi")
        meta_verbose_name = _("Yazar")
        meta_verbose_name_plural = _("Yazarlar")

    class BookPageStrings():
        book_verbose_name = _("Kitap")
        title_verbose_name = _("Sayfa Başlığı")
        content_verbose_name = _("Sayfa İçeriği")
        page_number_verbose_name = _("Sayfa Numarası")
        image_verbose_name = _("Görsel")
        image_position_verbose_name = _("Görselin Konumu")
        content_position_verbose_name = _("İçeriğin Konumu")
        image_position_verbose_name = _("Görselin Konumu")
        meta_verbose_name = _("Kitap Sayfası")
        meta_verbose_name_plural = _("Kitap Sayfaları")

    class ReadingHistoryStrings():
        book_verbose_name = _("Kitap")
        child_verbose_name = _("Çocuk")
        is_finished_verbose_name = _("Kitap bitirildi mi?")
        is_finished_false = _("Hayır")
        is_finished_true = _("Evet")
        counter_verbose_name = _("Okuma Sayacı")
        meta_verbose_name = _("Okuma Geçmişi")
        meta_verbose_name_plural = _("Okuma Geçmişleri")

    class PermissionStrings():
        is_own_child_permission = _("The person whose record you want to see must be your child.")
        is_parent_or_instructor = _("To see this page, you must be a parent or an instructor")
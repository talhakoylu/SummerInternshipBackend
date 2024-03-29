from django.utils.translation import ugettext_lazy as _

class BookStrings():
    class BookLanguageStrings():
        meta_verbose_name = _("dil")
        meta_verbose_name_plural = _("diller")
        language_name_verbose_name = _("Dil")
        language_code_verbose_name = _("Dil Kodu")
        language_code_help_text = _("Dil Kodu'nu <a href='http://www.lingoes.net/en/translator/langcode.htm'><strong>ISO Dil Kodları</strong></a> sayfasındaki kodlara uygun olarak giriniz. Bu kitap dinlerken okuyucunun tercüme dilini etkiliyor.")

    class AbstractBaseModelStrings():
        created_at_verbose_name = _("Oluşturulma Tarihi")
        updated_at_verbose_name = _("Güncellenme Tarihi")

    class CategoryStrings():
        title_verbose_name = _("Türkçe Başlık")
        english_title_verbose_name = _("İngilizce Başlık")
        description_verbose_name = _("Türkçe Açıklama")
        english_description_verbose_name = _("İngilizce Açıklama")
        meta_verbose_name = _("kategori")
        meta_verbose_name_plural = _("kategoriler")

    class BookLevelStrings():
        title_verbose_name = _("Başlık")
        english_title_verbose_name = _("İngilizce Başlık")
        meta_verbose_name = _("seviye")
        meta_verbose_name_plural = _("kitap seviyeleri")

    class BookStrings():
        category_verbose_name = _("Kategori")
        level_verbose_name = _("Seviye")
        language_verbose_name = _("Kitap Dili")
        name_verbose_name = _("İsim")
        description_verbose_name = _("Açıklama")
        author_verbose_name = _("Yazar")
        page_verbose_name = _("Sayfa Sayısı")
        cover_image_verbose_name = _("Kapak Görseli")
        meta_verbose_name = _("kitap")
        meta_verbose_name_plural = _("kitaplar")

    class Author():
        first_name_verbose_name = _("İsim")
        last_name_verbose_name = _("Soyisim")
        photo_verbose_name = _("Fotoğraf")
        biography_verbose_name = _("Biyografi")
        meta_verbose_name = _("yazar")
        meta_verbose_name_plural = _("yazarlar")

    class BookPageStrings():
        book_verbose_name = _("Kitap")
        title_verbose_name = _("Sayfa Başlığı")
        content_verbose_name = _("Sayfa İçeriği")
        page_number_verbose_name = _("Sayfa Numarası")
        image_verbose_name = _("Görsel")
        image_position_verbose_name = _("Görselin Konumu")
        content_position_verbose_name = _("İçeriğin Konumu")
        image_position_verbose_name = _("Görselin Konumu")
        meta_verbose_name = _("kitap sayfası")
        meta_verbose_name_plural = _("kitap sayfaları")
        text_inside_image = _("Is the Text inside the Image?")
        text_inside_image_help = _("If you choose this option, the text will be positioned inside the image. Otherwise, the center option of text position will be disabled in frontend.")

    class ReadingHistoryStrings():
        book_verbose_name = _("Kitap")
        child_verbose_name = _("Çocuk")
        is_finished_verbose_name = _("Kitap bitirildi mi?")
        is_finished_false = _("Hayır")
        is_finished_true = _("Evet")
        counter_verbose_name = _("Okuma Sayacı")
        meta_verbose_name = _("okuma geçmişi")
        meta_verbose_name_plural = _("okuma geçmişleri")
        exists_error = _("Bu kayıt daha önce eklendiği için yenisini ekleyemezsiniz, bunun yerine varolan kaydı düzenlemeyi deneyiniz.")

    class PermissionStrings():
        is_own_child_permission = _("The person whose record you want to see must be your child.")
        is_parent_or_instructor = _("To see this page, you must be a parent or an instructor")
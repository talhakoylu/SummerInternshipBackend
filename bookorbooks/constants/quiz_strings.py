from django.utils.translation import ugettext_lazy as _

class QuizStrings():
    class AbstractBaseStrings():
        created_at_verbose_name = _("Oluşturulma Tarihi")
        updated_at_verbose_name = _("Güncellenme Tarihi")

    class QuizStrings():
        book_verbose_name = _("Kitap")
        title_verbose_name = _("Başlık")
        enabled_verbose_name = _("Sınav Aktif Mi?")
        meta_quiz_verbose_name = _("Sınav")
        meta_quiz_verbose_name_plural = _("Sınavlar")

    class QuestionStrings():
        quiz_verbose_name = _("Sınav")
        question_verbose_name = _("Soru")
        topic_verbose_name = _("Konu")
        topic_hint_text = _("Rapor sayfasında, cevabın yanlış olması durumunda gösterilecek metin.")
        meta_question_verbose_name = _("Soru")
        meta_question_verbose_name_plural = _("Sorular")

    class AnswerStrings():
        answer_verbose_name = _("Cevap")
        question_verbose_name = _("Soru")
        is_correct_verbose_name = _("Doğru Bir Cevap Mı?")
        meta_answer_verbose_name = _("Cevap")
        meta_answer_verbose_name_plural = _("Cevaplar")

    class TakingQuizStrings():
        quiz_verbose_name = _("Sınav")
        child_verbose_name = _("Çocuk")
        title_verbose_name = _("Başlık")
        total_point_verbose_name = _("Toplam Puan")
        meta_verbose_name = _("Çözülmüş Sınav Kaydı") 
        meta_verbose_name_plural = _("Çözülmüş Sınav Kayıtları")
    
    class TakingQuizAnswersStrings():
        taking_quiz_verbose_name = _("Girilen Sınav")
        taking_quiz_title_verbose_name = _("Girilen Sınav Başlığı")
        question_verbose_name = _("Soru")
        question_topic_verbose_name = _("Sorunun Konusu")
        answer_verbose_name = _("Cevap")
        answer_is_correct_verbose_name = _("Cevap Doğru Mu?")
        total_point_verbose_name = _("Toplam Puan")
        meta_verbose_name = _("Çözülmüş Sınav Cevabı") 
        meta_verbose_name_plural = _("Çözülmüş Sınav Cevapları")

    class ValidationErrorMessages():
        answer_is_not_belong_to_question = _("This answer does not belong to the question you chose, please check it.")
        question_is_not_belong_to_quiz = _("This question does not belong to the exam you chose, please check it.")
        reading_must_finished = _("To solve the book quiz, you must finish reading that book.")
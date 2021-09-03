# Generated by Django 3.2.5 on 2021-09-02 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20210730_1357'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='takingquiz',
            options={'verbose_name': 'çözülmüş sınav kaydı', 'verbose_name_plural': 'çözülmüş sınav kayıtları'},
        ),
        migrations.AlterModelOptions(
            name='takingquizanswer',
            options={'verbose_name': 'çözülmüş sınav cevabı', 'verbose_name_plural': 'çözülmüş sınav cevapları'},
        ),
        migrations.AlterField(
            model_name='quiz',
            name='enabled',
            field=models.BooleanField(choices=[(True, 'Aktif'), (False, 'Aktif Değil')], default=False, help_text="<p>Bir kitap birden fazla sınava sahip olabilir, hangi sınavın kullanıcıya gözükeceğini <b>Sınav Aktif Mi?</b> seçeneği ile belirleyebilirsiniz. Seçtiğiniz kitaba ait <span style ='color: red; font-weight: bold;'>aktif sınav</span> sayısının 1 olduğundan emin olunuz. Eğer birden fazla aktif sınav varsa, kullanıcı tarafında <span style ='color: red; font-weight: bold;'>aktif son sınav</span> kullanıcıya gösterilir.</p>", verbose_name='Sınav Aktif Mi?'),
        ),
        migrations.AlterField(
            model_name='takingquiz',
            name='total_point',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Toplam Puan'),
        ),
    ]

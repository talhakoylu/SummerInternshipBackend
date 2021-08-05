# Generated by Django 3.2.5 on 2021-07-28 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_instructorprofile'),
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
                ('is_finished', models.BooleanField(choices=[(False, 'Hayır'), (True, 'Evet')], verbose_name='Kitap bitirildi mi?')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_reading_history', to='book.book', verbose_name='Kitap')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_reading_history', to='account.childprofile', verbose_name='Çocuk')),
            ],
            options={
                'verbose_name': 'Okuma Geçmişi',
                'verbose_name_plural': 'Okuma Geçmişleri',
            },
        ),
    ]
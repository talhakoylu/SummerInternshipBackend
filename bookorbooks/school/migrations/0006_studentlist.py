# Generated by Django 3.2.5 on 2021-07-23 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_instructorprofile'),
        ('school', '0005_alter_class_instructor'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children_class', to='account.childprofile', verbose_name='Öğrenci/Çocuk')),
                ('school_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_list_class', to='school.class', verbose_name='Okul')),
            ],
            options={
                'verbose_name': 'Sınıf Öğrencisi',
                'verbose_name_plural': 'Sınıf Öğrencileri',
            },
        ),
    ]
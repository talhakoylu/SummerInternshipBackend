# Generated by Django 3.2.5 on 2021-09-02 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_instructorprofile_principal'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='childlist',
            options={'verbose_name': 'ebeveyn ve çocuk kaydı', 'verbose_name_plural': 'ebeveyn ve çocuk kayıtları'},
        ),
        migrations.AlterModelOptions(
            name='childprofile',
            options={'verbose_name': 'çocuk', 'verbose_name_plural': 'çocuklar'},
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'kullanıcı', 'verbose_name_plural': 'kullanıcılar'},
        ),
        migrations.AlterModelOptions(
            name='instructorprofile',
            options={'verbose_name': 'eğitmen', 'verbose_name_plural': 'eğitmenler'},
        ),
        migrations.AlterModelOptions(
            name='parentprofile',
            options={'verbose_name': 'ebeveyn', 'verbose_name_plural': 'ebeveynler'},
        ),
    ]

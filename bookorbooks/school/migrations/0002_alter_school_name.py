# Generated by Django 3.2.5 on 2021-07-14 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Okul Adı'),
        ),
    ]

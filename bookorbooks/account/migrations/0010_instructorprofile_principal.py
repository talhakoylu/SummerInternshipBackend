# Generated by Django 3.2.5 on 2021-08-24 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_instructorprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructorprofile',
            name='principal',
            field=models.BooleanField(default=False, verbose_name='Müdür'),
        ),
    ]

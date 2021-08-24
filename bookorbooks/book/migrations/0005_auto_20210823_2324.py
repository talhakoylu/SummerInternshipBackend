# Generated by Django 3.2.5 on 2021-08-23 23:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_auto_20210812_0751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookpage',
            name='image_position',
        ),
        migrations.AddField(
            model_name='bookpage',
            name='text_inside_image',
            field=models.BooleanField(default=False, help_text='If you choose this option, the text will be positioned inside the image. Otherwise, the center option of text position will be disabled in frontend.', verbose_name='Is the Text inside the Image?'),
        ),
        migrations.AlterField(
            model_name='bookpage',
            name='content_position',
            field=models.SmallIntegerField(choices=[(1, 'Orta'), (0, 'Üst'), (2, 'Alt')], default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)], verbose_name='İçeriğin Konumu'),
        ),
        migrations.AlterField(
            model_name='bookpage',
            name='page_number',
            field=models.PositiveIntegerField(default=0, verbose_name='Sayfa Numarası'),
            preserve_default=False,
        ),
    ]

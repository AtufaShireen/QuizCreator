# Generated by Django 3.1.4 on 2021-05-26 11:27

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20210526_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizzer',
            name='bg_pic',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='bg_pic'),
        ),
    ]

# Generated by Django 3.1.4 on 2021-04-26 08:52

from django.db import migrations
import quiz.models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='answer',
            field=quiz.models.RangeField(default=1, max_val=4, min_val=1, verbose_name='correct option'),
        ),
    ]

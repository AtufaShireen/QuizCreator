# Generated by Django 3.1.4 on 2021-03-31 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_auto_20210330_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizzer',
            name='reattempt',
            field=models.BooleanField(default=True),
        ),
    ]
# Generated by Django 3.1.4 on 2021-03-30 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_auto_20210320_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizscore',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='score_quiz', to='quiz.quizzer'),
        ),
    ]
# Generated by Django 3.1.4 on 2021-04-10 08:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0013_quizzer_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizzer',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]

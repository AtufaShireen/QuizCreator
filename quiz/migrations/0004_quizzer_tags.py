# Generated by Django 3.1.4 on 2021-03-14 13:39

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('quiz', '0003_auto_20210313_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizzer',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]

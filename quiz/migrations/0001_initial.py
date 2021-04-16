# Generated by Django 3.1.4 on 2021-04-16 16:07

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UUIDTaggedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.UUIDField(db_index=True, verbose_name='object ID')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_uuidtaggeditem_tagged_items', to='contenttypes.contenttype', verbose_name='content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_uuidtaggeditem_items', to='taggit.tag')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Quizzer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('title', models.CharField(max_length=250, unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('bg_pic', models.ImageField(default='def.png', upload_to='quiz_pic')),
                ('reattempt', models.BooleanField(default=True, verbose_name='Allow Reattempt')),
                ('private', models.BooleanField(default=False, verbose_name='Make private')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='quiz.UUIDTaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_quiz', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuizScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='score_quiz', to='quiz.quizzer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('question', models.CharField(default='', max_length=1024)),
                ('option_1', models.CharField(default='', max_length=1024)),
                ('option_2', models.CharField(default='', max_length=1024)),
                ('option_3', models.CharField(default='', max_length=1024)),
                ('option_4', models.CharField(default='', max_length=1024)),
                ('answer', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='correct option')),
                ('quizz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizz_question', to='quiz.quizzer')),
            ],
        ),
        migrations.CreateModel(
            name='AnonymousUsersData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=25)),
                ('score', models.IntegerField(default=0)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quizzer')),
            ],
        ),
    ]

# postgres://rkbvpbvhmhwpkl:dfdbee0878911220a024455cd4b11c5f66984a1607c8b2be30a7f1ce58d5e090@ec2-52-86-116-94.compute-1.amazonaws.com:5432/dbt1750f8sgc33
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Quizzer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_quiz')
    title = models.CharField(max_length=250, null=False)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def all_question(self):
        print('------------------this was called!')
        return self.questions_set.all()

    @property
    def question_count(self):
        return self.Questions.quizz_question.count()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Quizzer, self).save(*args, **kwargs)


class Questions(models.Model):
    quizz = models.ForeignKey('Quizzer',on_delete=models.CASCADE,related_name='quizz_question')
    slug = models.SlugField(null=True, blank=True)
    question = models.CharField(max_length=1024, default='')
    option_1=models.CharField(max_length=1024, default='')
    option_2=models.CharField(max_length=1024, default='')
    option_3=models.CharField(max_length=1024, default='')
    option_4=models.CharField(max_length=1024, default='')
    answer=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)],default=1)

    def __str__(self):
        return f'{self.question}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.question)

        super(Questions, self).save(*args, **kwargs)

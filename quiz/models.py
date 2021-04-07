from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager

# class CustomQuerySet(models.QuerySet):
#     def private(self):
#         return self.filter(private=True)

#     def public(self):
#         return self.filter(private=False)

# class CustomQueryManager(models.Manager):
#     def get_queryset(self):
#         return CustomQuerySet(self.model, using=self._db)

#     def private(self):
#         return self.get_queryset().private()

#     def public(self):
#         return self.get_queryset().public()

class Quizzer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_quiz')
    title = models.CharField(max_length=250, null=False,unique=True)
    slug = models.SlugField(null=True, blank=True)
    bg_pic = models.ImageField(default='def.png', upload_to='quiz_pic')
    reattempt=models.BooleanField(default=True,verbose_name='Allow Reattempt')
    private=models.BooleanField(default=False,verbose_name='Make private')
    tags=TaggableManager()
    objects = models.Manager() #default manager
    # custom_objects=CustomQueryManager()

    def user_quizzes(self):
        return self.user.user_quiz.count()
    def __str__(self):
        return self.title

    @property
    def all_question(self):
        return self.quizz_question.all()
    @property
    def all_tags(self):
        return [i.name for i in self.tags.all()]

    @property
    def question_count(self):
        return self.quizz_question.count()

    def get_absolute_url(self):
        return reverse('quiz:quizz',kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
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
    answer=models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)],default=1,verbose_name='correct option')

    def __str__(self):
        return f'{self.question}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question)

        super(Questions, self).save(*args, **kwargs)

class QuizScore(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    quiz=models.ForeignKey(Quizzer, on_delete=models.CASCADE,related_name='score_quiz')
    score=models.IntegerField(default=0)
    @property
    def quizzie_score(self):
        return (self.quiz.title) # ,self.score
    def __str__(self):
        return f"{self.user}'s score{self.score}"
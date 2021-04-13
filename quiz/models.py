from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase
import uuid

class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

class Quizzer(models.Model):
    id=models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_quiz')
    title = models.CharField(max_length=250, null=False,unique=True)
    slug = models.SlugField(null=True, blank=True)
    bg_pic = models.ImageField(default='def.png', upload_to='quiz_pic')
    reattempt=models.BooleanField(default=True,verbose_name='Allow Reattempt')
    private=models.BooleanField(default=False,verbose_name='Make private')
    tags=TaggableManager(through=UUIDTaggedItem)
    objects = models.Manager() #default manager
    # custom_objects=CustomQueryManager()

    
    @property
    def user_quizzes(self): # Quizzes By this User
        return self.user.user_quiz.count()
    def __str__(self):
        return self.title

    @property
    def all_question(self): #all questions of the quiz
        return self.quizz_question.all()
    @property
    def all_tags(self): # all tags of this quiz
        return [i.name for i in self.tags.all()]

    @property 
    def attempters(self): # numbers of users atempted this quiz
        return self.score_quiz.count()

    def user_tags(self): # unique tags used ny the creator
        g=[]
        for i in self.user.user_quiz.all():
            for j in i.all_tags:
                if j not in g:
                    g.append(j)
        return g
    @property
    def question_count(self): # number of questions on the quiz
        return self.quizz_question.count()
    
    def all_attempters(self):
        return self.score_quiz.all()

    def get_absolute_url(self):
        return reverse('quiz:quizz',kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Quizzer, self).save(*args, **kwargs)

# class Usertags(models.Model):
    '''works with signals but upgrade to python 3.9 for JSOn Field or update sql'''
#     user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="user_tags")
#     tags=models.JSONField(null=True) upgrade to python 3.9


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
    user=models.ForeignKey(User, on_delete=models.CASCADE) #could be onetoone as well
    quiz=models.ForeignKey(Quizzer, on_delete=models.CASCADE,related_name='score_quiz') 
    score=models.IntegerField(default=0)
    @property
    def quizzie_score(self): # title of the score
        return (self.quiz.title) # ,self.score
    def __str__(self):
        return f"{self.user}'s score{self.score}"
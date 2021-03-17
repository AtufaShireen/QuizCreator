from django.contrib import admin
from .models import Questions,Quizzer


class QuizAmin(admin.ModelAdmin):
    list_display = ('id','title', 'tags', 'user')
    list_filter = ('tags', )
class QuesAmin(admin.ModelAdmin):
    list_display = ('id','question', 'quizz')
    list_filter = ('quizz', )   

admin.site.register(Quizzer, QuizAmin) 
admin.site.register(Questions, QuesAmin) 
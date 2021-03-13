from django.contrib import admin
from .models import Questions,Quizzer
admin.site.register([Quizzer,Questions])
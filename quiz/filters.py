from .models import Quizzer
import django_filters

class QuizFilter(django_filters.FilterSet):
    title=django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Quizzer
        fields = ['tags__name','title']
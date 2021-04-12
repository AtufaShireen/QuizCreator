from .models import Quizzer
import django_filters

class QuizFilter(django_filters.FilterSet):
    # tags__name=django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Quizzer
        fields = ['tags__name']
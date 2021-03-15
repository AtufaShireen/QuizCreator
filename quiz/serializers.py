from rest_framework import serializers
from .models import Quizzer, Questions


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['question','option_1','option_2','option_3','option_4','answer']


class QuizzerSerializer(serializers.ModelSerializer):
  
    n_questions = serializers.CharField(source='question_count', read_only=True)
    tags=serializers.CharField(source='all_tags', read_only=True)
    class Meta:
        model = Quizzer
        fields = ['id','title','n_questions','tags'] # 
        depth=1

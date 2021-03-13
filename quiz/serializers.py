from rest_framework import serializers
from .models import Quizzer, Questions



class QuestionSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source='quizz.title', read_only=True)

    class Meta:
        model = Questions
        fields = ['quiz_title','question','option_1','option_2','option_3','option_4','answer']


class QuizzerSerializer(serializers.ModelSerializer):
    n_questions = serializers.SerializerMethodField(method_name='all_questions')

    class Meta:
        model = Quizzer
        fields = ['id','title','n_questions'] # 

    def all_questions(self, instance):
        return instance.quizz_question.count()

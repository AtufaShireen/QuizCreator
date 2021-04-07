from rest_framework import serializers
from .models import Quizzer, Questions,QuizScore

class ProfileSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source='user.username', read_only=True)
    n_quizzes = serializers.CharField(source='user_quizzes', read_only=True)
    class Meta:
        model=Quizzer
        fields=['username','n_quizzes']

class QuizzerSerializer(serializers.ModelSerializer):
    
    n_questions = serializers.CharField(source='question_count', read_only=True)
    tags=serializers.CharField(source='all_tags', read_only=True)
    class Meta:
        model = Quizzer
        fields = ['title','n_questions','tags']
        depth=1
       
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['question','option_1','option_2','option_3','option_4','answer']

class UserAttemptedQuizes(serializers.ModelSerializer):
    title=serializers.CharField(source='quizzie_score', read_only=True)
    class Meta:
        model=QuizScore
        fields=['title','score']

#apple.tags.slugs()
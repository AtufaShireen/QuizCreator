from rest_framework import serializers
from .models import Quizzer, Questions,QuizScore

class ProfileSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source='user.username', read_only=True)
    bio=serializers.CharField(source='user.bio', read_only=True)
    n_quizzes = serializers.CharField(source='user_quizzes', read_only=True)
    tags_used=serializers.CharField(source='user_tags')

    class Meta:
        model=Quizzer
        fields=['username','n_quizzes','bio','tags_used']

class QuizzerSerializer(serializers.ModelSerializer):
    
    n_questions = serializers.CharField(source='question_count', read_only=True)
    tags=serializers.JSONField(source='all_tags', read_only=True)
    attempted_by=serializers.CharField(source='attempters', read_only=True)
    class Meta:
        model = Quizzer
        fields = ['title','n_questions','tags','attempted_by','reattempt','private']
        depth=1
       
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['question','option_1','option_2','option_3','option_4','answer','points']

class UserAttemptedQuizes(serializers.ModelSerializer):
    title=serializers.CharField(source='quizzie_score', read_only=True)
    class Meta:
        model=QuizScore
        fields=['title','score']


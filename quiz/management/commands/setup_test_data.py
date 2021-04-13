import random
from django.db import transaction
from django.contrib.auth.models import User
from quiz.models import Quizzer,Questions,QuizScore
from quiz.factories import UserFactory,QuizzerFactory,QuestionFactory,QuizScoreFactory
from django.core.management.base import BaseCommand
NUM_USERS=7
NUM_QUIZ=8 
NUM_QUES=32
NUM_QUIZ_SCORE=16

class Command(BaseCommand):
    help='Generates test data'

    @transaction.atomic
    def handle(self,*args,**kwargs):
        self.stdout.write("Deleting old data")
        models=[User,Quizzer,Questions,QuizScore]
        for m in models:
            m.objects.all().delete()
        self.stdout.write("Creating new data...")

        
        # Create all the users
        users = []
        for _ in range(NUM_USERS):
            users.append(UserFactory())
        
        # add questions
        quests=[]
        for _ in range(NUM_QUES):
            ques=QuestionFactory()
            quests.append(ques)
        q = list(zip(*[iter(quests)]*4) )# spilt questions into chunks of 4s
        
        #add quizzes
        quizzies=[]
        for i in range(NUM_QUIZ):
            people=random.choice(users)
            QuizzerFactory(user=people)
            
            quiz=QuizzerFactory(user=people)
            quiz.quizz_question.add(*q[i])
            quizzies.append(quiz)
        
        #adding random scores
        for _ in range(NUM_QUIZ_SCORE):
            user=random.choice(users)
            quiz=random.choice(quizzies)
            QuizScoreFactory(user=user,quiz=quiz,score=random.randint(1,4))
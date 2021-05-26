import factory
from factory.fuzzy import FuzzyInteger
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from .models import Quizzer,Questions,QuizScore
from faker import Faker
fake=Faker()

class UserFactory(DjangoModelFactory):
    class Meta:
        model=User
    class Params:
        naame=factory.Faker('name')
    username=factory.LazyAttribute(lambda a: a.naame)

class QuizzerFactory(DjangoModelFactory):
    model=Quizzer
    # class Params:
    #     tage=factory.Faker('word')
    
    tags=[factory.Faker('name') for _ in range(3)]
    user=factory.SubFactory(UserFactory)
    title=factory.Faker(
        "sentence",
        nb_words=5,
        variable_nb_words=True    
    )
    reattempt=factory.Faker("pybool")
    private=False#factory.Faker("pybool")
    

class QuestionFactory(DjangoModelFactory):
    class Meta:
        model=Questions
    quizz=factory.SubFactory(QuizzerFactory)
    question=factory.Faker(
        "paragraph",
        nb_sentences=5,
        variable_nb_sentences=False # not exact number of words    
    )
    option_1=factory.Faker(
        "sentence",
        nb_words=5,
        variable_nb_words=True    
    )
    option_2=factory.Faker(
        "sentence",
        nb_words=5,
        variable_nb_words=True    
    )
    option_3=factory.Faker(
        "sentence",
        nb_words=5,
        variable_nb_words=True    
    )
    option_4=factory.Faker(
        "sentence",
        nb_words=5,
        variable_nb_words=True    
    )
    answer=FuzzyInteger(1,4)
    points=FuzzyInteger(1,10)


class QuizScoreFactory(DjangoModelFactory):
    class Meta:
        model=QuizScore
    user=factory.SubFactory(UserFactory)
    quiz=factory.SubFactory(QuizzerFactory)
    score=FuzzyInteger(1,4)
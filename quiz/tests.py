from django.test import TestCase
from django.contrib.auth.models import User
from .models import Quizzer,Questions,QuizScore
from django.urls import reverse
# from model_bakery import baker
class QuizzerTestCase(TestCase):  
    def setUp(self):  
        user=User.objects.create(username='Atufa')
        x=Quizzer.objects.create(user=user, title="Animal Sounds",reattempt=False) #tags=['lion','cat']
        x.save()
        tag1 = x.tags.create(name="lion")
        tag1.save()
        tag2 = x.tags.create(name="tiger")
        tag2.save()
        y=Questions.objects.create(
            quizz=x,
            question='whose sound is this?..roar..',
            option_1="lion",
            option_2="tiger",
            option_3="cat",
            option_4="leopard",
            answer=1
        )
        z=Questions.objects.create(
            quizz=x,
            question='whose sound is this?..meow..',
            option_1="lion",
            option_2="tiger",
            option_3="cat",
            option_4="leopard",
            answer=3
        )
    
        # event = baker.make(Quizzer, title="Animal Sounds")
    def test_quiz_created(self):
        lion = Quizzer.objects.get(title="Animal Sounds")
        x = Questions.objects.get(question='whose sound is this?..meow..')
        self.assertEqual(lion.slug, "animal-sounds")
        self.assertEqual(lion.question_count, 2)
        # self.assertEqual(lion.tags.all(), ["lion",'tiger'])
        # self.assertEqual(lion.all_tags, ["lion",'tiger'])
        self.assertEqual(str(lion), "Animal Sounds")
        self.assertEqual(x.slug, "whose-sound-is-thismeow")
        self.assertEqual(str(x), "whose sound is this?..meow..")
        

class TestCreateQuizView(TestCase):
    def test_anonymous_cannot_create_edit__quiz(self):
        response = self.client.get(reverse("quiz:create-quiz"))
        self.assertRedirects(response, "/login/?next=/quiz/add/")
        response = self.client.get(reverse("quiz:update-quiz",args=['my sound']))
        self.assertRedirects(response, "/login/?next=/quiz/edit/my%2520sound/")

class TestQuizCreateForm(TestCase):
    def test_create_quiz(self):
        user=User.objects.create(username="Atufaaa")
        self.client.force_login(user=user)
        data = {
            "user": user.id,
            "title": "Animal Sounds",
            "tags": " lion,tiger,cat",
            "quizz_question-TOTAL_FORMS": 2,
            "quizz_question-INITIAL_FORMS": 0,
            "quizz_question-0-question": "Whose sound?..meow..",
            "quizz_question-0-option_1":"Cat",
            "quizz_question-0-option_2":"Mouse",
            "quizz_question-0-option_3":"Rat",
            "quizz_question-0-option_4":"Bill",
            "quizz_question-0-answer":"1",
            "quizz_question-1-question": "Whose sound?..roar..",
            "quizz_question-1-option_1":"Cat",
            "quizz_question-1-option_2":"Mouse",
            "quizz_question-1-option_3":"Rat",
            "quizz_question-1-option_4":"Lion",
            "quizz_question-1-answer":"4",
        }
        response = self.client.post("/quiz/add/", data=data)
        self.assertEqual(Quizzer.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/quizzes/")


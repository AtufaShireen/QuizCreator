from django.urls import path, include
from .views import QuizzView, QuizzesView,create_quiz_form,update_quiz_form,QuizzApiView,QuizzesApiView #QuizCreateView,

urlpatterns = [
    path('quiz/add/',create_quiz_form, name='create-quiz'),
    path('quiz/edit/<int:quizzer_id>/', update_quiz_form, name='update-quiz'),
    path('quizzes/', QuizzesView.as_view(), name='quizzes'),
    path('quiz/<str:slug>/', QuizzView.as_view(), name='quizz'),
    path('api-auth/',include('rest_framework.urls')),
    path('api-auth/quizzes/', QuizzesApiView.as_view(), name='api-quizzes'),
    path('api-auth/quiz/<str:slug>/', QuizzApiView.as_view(), name='api-quizz'),
]
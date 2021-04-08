from django.urls import path, include
from .views import QuizzView, Quizzes,edit_quiz_form,add_quiz_form,QuizzApiView,UserProfileApiView, \
  QuizzesApiView,UserQuizzesApiView
app_name='quiz'
urlpatterns = [
    path('quiz/add/',add_quiz_form, name='create-quiz'),
    path('quiz/edit/<str:quiz_tit>/', edit_quiz_form, name='update-quiz'),
    path('', Quizzes, name='quizzes'),
    path('quiz/<str:slug>/', QuizzView, name='quizz'),
    path('api-auth/',include('rest_framework.urls')),
    path('api-auth/quizzes/', QuizzesApiView.as_view(), name='api-quizzes'),
    path('api-auth/profile/', UserQuizzesApiView.as_view(), name='api-user-quizzes'),
    path('api-auth/profile/<str:username>/', UserProfileApiView.as_view(), name='api-profile-quizzes'),
    path('api-auth/quiz/<str:slug>/', QuizzApiView.as_view(), name='api-quizz'),
]
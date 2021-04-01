from django.urls import path, include
from .views import QuizzView, Quizzes,quiz_form,QuizzApiView,QuizzesApiView,AttemptedQuizzApiView,UserQuizzesApiView
app_name='quiz'
urlpatterns = [
    path('quiz/add/',quiz_form, name='create-quiz'),
    path('quiz/edit/<str:quizzer_id>/', quiz_form, name='update-quiz'),
    path('quizzes/', Quizzes, name='quizzes'),
    path('quiz/<str:slug>/', QuizzView, name='quizz'),
    path('api-auth/',include('rest_framework.urls')),
    path('api-auth/quizzes/', QuizzesApiView.as_view(), name='api-quizzes'),
    path('api-auth/user/attempted/quizzes/', AttemptedQuizzApiView.as_view(), name='api-attempted-quizzes'),
    path('api-auth/user/created/quizzes/', UserQuizzesApiView.as_view(), name='api-user-quizzes'),
    path('api-auth/quiz/<str:slug>/', QuizzApiView.as_view(), name='api-quizz'),
]
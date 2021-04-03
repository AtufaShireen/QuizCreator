from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from .models import Questions, Quizzer,QuizScore
from .serializers import QuizzerSerializer, QuestionSerializer,UserAttemptedQuizes
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView, Response
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import QuestionsFormset,QuizForm
from .filters import QuizFilter
from django.db.models import Q
from django.contrib.auth.decorators import login_required
@login_required
def quiz_form(request, quiz_tit=None):
    try:
        inst=Quizzer.objects.get(slug=quiz_tit)
    except Quizzer.DoesNotExist:
        inst=None
        
    quiz_form=QuizForm(request.POST or None,request.FILES or None,instance=inst)
    ques_fromset=QuestionsFormset(request.POST or None,instance=inst)
    
    if ques_fromset.is_valid() and quiz_form.is_valid():
        quiz_instance=quiz_form.save(commit=False)
        quiz_instance.user=request.user
        quiz_instance.save()
        quiz_form.save_m2m()
        instance = ques_fromset.save(commit=False)
        for i in instance:  
            i.quizz=quiz_instance        
        for i in instance:
            i.save()
        return redirect('/quizzes/')
  
    return render(request, 'quiz/create-quiz.html', {'quest_form': ques_fromset,'quiz_form':quiz_form}) #create-quiz

def QuizzView(request,slug):
    quiz=Quizzer.objects.get(slug=slug)
    questions=quiz.all_question
    context={'quiz':quiz,'questions':questions}
    if request.method=='POST':
        counter=0
        for i in questions:
            if i.answer==int(request.POST[i.question]):
                counter+=1
            else:
                print('actual answer was',i.answer,'selected answer was',request.POST[i.question]) 
        try:
            print('----------------main thingie here-----')
            add_score=QuizScore.objects.get(user=request.user,quiz=quiz)
            print('---------yes,,,,,,,,already attempted quiz herer...')
            add_score.score=counter
            add_score.save()
        except QuizScore.DoesNotExist:
            print('-------------not attempted this quiz')
            add_score=QuizScore(user=request.user,quiz=quiz,score=counter)
            add_score.save()
        messages.success(request, f'Your Score was {counter}')
        return redirect('quiz:quizzes')
    return render(request,'quiz/quiz.html',context=context)

def ResultPage(requests,score):
    return HttpResponse(f'Your Score Was..{score}')

def Quizzes(request):
    if request.user.is_authenticated:
        query=Quizzer.objects.exclude(user=request.user)
    else:
        query=Quizzer.objects.all()
    Filter=QuizFilter(request.GET,queryset=query)
    context={'quizzes':query,'filter':Filter}
    return render(request,'quiz/quizzes.html',context)


class QuizzesApiView(ListAPIView):
    serializer_class = QuizzerSerializer
    queryset = Quizzer.objects.all()


class QuizzApiView(APIView):
    def get(self, request, format=None, **kwargs):
        quiz = get_object_or_404(Quizzer, slug__iexact=kwargs['slug'])  # case insensitive LIKE clause
        questions = Questions.objects.filter(quizz=quiz)
        serializer = QuestionSerializer(questions, many=True)  # add related name to the models for working
        return Response(serializer.data)

class AttemptedQuizzApiView(APIView):
    def get(self, request, format=None, **kwargs):
        quizzes = QuizScore.objects.filter(user=self.request.user)
        serializer = UserAttemptedQuizes(quizzes, many=True)  # add related name to the models for working
        return Response(serializer.data)

class UserQuizzesApiView(APIView):
    def get(self, request, format=None, **kwargs):
        quizzes = Quizzer.objects.filter(user=self.request.user)
        serializer = QuizzerSerializer(quizzes, many=True)  # add related name to the models for working
        return Response(serializer.data)
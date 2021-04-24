from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse,get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from .models import Questions, Quizzer,QuizScore,AnonymousUsersData
from django.contrib.auth.models import User
from .serializers import  QuestionSerializer,UserAttemptedQuizes ,QuizzerSerializer,ProfileSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView, Response
from django.contrib import messages
from .forms import QuestionsFormset,QuizForm
from .filters import QuizFilter
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.http import Http404
def error_404(request,exception):
    data={}
    return render(request,'quiz/404.html', data)

def ShareQuizzView(request,id,username,quiz_name): # modify to check 404 and private
    try:
        
        quiz=Quizzer.objects.get(slug=quiz_name,user__username=username,uuid=id)
        if request.user!=quiz.user and quiz.private==True:
            raise Http404()
    except Quizzer.DoesNotExist:
        messages.warning(request,'Quiz Does not exists')
        raise Http404()
    questions=quiz.all_question
    context={'quiz':quiz,'questions':questions,'shared':True}
    if request.method=='POST':
        if request.user.is_authenticated:
            if quiz.user==request.user:
                return redirect('quiz:quizzes')
            return redirect('quiz:quizz',slug=quiz_name)
        if len(request.POST)!=len(questions)+2:
            messages.warning(request, 'Answer all the questions')
            return redirect('quiz:share-view',uuid=id,quiz_name=quiz_name,username=username)
        
        name=request.POST.get('name','')
        counter=0
        for i in questions:
            if i.answer==int(request.POST[i.question]):
                counter+=1
            else:
                pass
        AnonymousUsersData(user=name,score=counter,quiz=quiz)
        messages.success(request, f'Your Score was {counter}')
    return render(request,'quiz/quiz.html',context=context)

@login_required
def add_quiz_form(request): 
    quiz_form=QuizForm(request.POST or None,request.FILES or None)
    ques_fromset=QuestionsFormset(request.POST or None)
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
        return redirect('quiz:quizzes')
  
    return render(request, 'quiz/create-quiz.html', {'quest_form': ques_fromset,'quiz_form':quiz_form}) #create-quiz

@login_required
def edit_quiz_form(request, quiz_tit=None):
    try:
        inst=Quizzer.objects.get(slug=quiz_tit)
        if inst.user!=request.user:
            messages.warning(request, f'Quiz Doesnot Exists')
            raise Http404()
    except Quizzer.DoesNotExist:
        messages.warning(request, f'Quiz Doesnot Exists')
        raise Http404()
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
        return redirect('quiz:quizzes')
    
  
    return render(request, 'quiz/create-quiz.html', {'quest_form': ques_fromset,'quiz_form':quiz_form}) #create-quiz


@login_required
def QuizzView(request,slug): # modify to check 404 and private
    try:
        quiz=Quizzer.objects.get(slug=slug)
        if request.user!=quiz.user and quiz.private==True:
            raise Http404()
    except Quizzer.DoesNotExist:
        messages.warning(request,'Quiz Does not exists')
        raise Http404()
    questions=quiz.all_question
    context={'quiz':quiz,'questions':questions}
    if request.method=='POST':
        if len(request.POST)!=len(questions)+1:
            messages.warning(request, 'Answer all the questions')
            return redirect('quiz:quizz',slug)
        counter=0
        for i in questions:
            if i.answer==int(request.POST[i.question]):
                counter+=int(request.POST[i.points])
            else:
                pass
        try:
            add_score=QuizScore.objects.get(user=request.user,quiz=quiz)
            add_score.score=counter
            add_score.save()
        except QuizScore.DoesNotExist:
            add_score=QuizScore(user=request.user,quiz=quiz,score=counter)
            add_score.save()
        messages.success(request, f'Your Score was {counter}')
        return redirect('quiz:quizzes')
    return render(request,'quiz/quiz.html',context=context)

# def ResultPage(requests,score):
#     return HttpResponse(f'Your Score Was..{score}')

def Quizzes(request):
    if request.user.is_authenticated:
        try: 
            ats=QuizScore.objects.filter(user=request.user).values_list('quiz_id') # to remove attempted quizzes
            query=Quizzer.objects.filter(Q(private=False)&~Q(user=request.user)&~Q(id__in=ats)) 
        except:
            # x= Quizzer.objects.prefetch_related('score_quiz').filter(user=request.user)
            query=Quizzer.objects.filter(Q(private=False)&~Q(user=request.user)) 
        

    else:
        query=Quizzer.objects.filter(Q(private=False))
    Filter=QuizFilter(request.GET,queryset=query)
    context={'quizzes':query,'filter':Filter}
    return render(request,'quiz/quizzes.html',context)


class QuizzesApiView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = QuizzerSerializer
    queryset = Quizzer.objects.all()

class UserQuizzesApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, **kwargs):    
        private=Quizzer.objects.filter(Q(private=True),Q(user=request.user))
        public=Quizzer.objects.filter(Q(private=False),Q(user=request.user))
        attempted = QuizScore.objects.filter(user=self.request.user)
        attempt_serializer = UserAttemptedQuizes(attempted, many=True)
        pri_serializer = QuizzerSerializer(private, many=True)
        pub_serializer = QuizzerSerializer(public, many=True)
        try:    
            if len(public)==0:
                quizzes=private[0]
            else:
                quizzes=public[0]
        except:
            quizzes=None

        prof_serializer=ProfileSerializer(quizzes)
        return Response({
            'Profile':prof_serializer.data,
            'attempted Quizzes':attempt_serializer.data,
            'Private Quizzes':pri_serializer.data,
            'Public Quizzes':pub_serializer.data,
            })
class UserProfileApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, **kwargs):
        user=kwargs.pop('username')
        try:
            user=User.objects.get(username=user)
        except User.DoesnotExists:
            print('dgj')
            raise Http404
        attempted = QuizScore.objects.filter(user=user)
        attempt_serializer = UserAttemptedQuizes(attempted, many=True)
        public=Quizzer.objects.filter(Q(private=False),Q(user=user))
        pub_serializer = QuizzerSerializer(public, many=True)
        try:    
            if len(public)==0:
                quizzes=private[0]
            else:
                quizzes=public[0]
        except:
            quizzes=None
        
        prof_serializer=ProfileSerializer(quizzes)
        
        return Response({
            'Profile':prof_serializer.data,
            'attempted Quizzes':attempt_serializer.data,
            'Public Quizzes':pub_serializer.data,
            })


class QuizzApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, **kwargs):
        quiz = get_object_or_404(Quizzer, slug__iexact=kwargs['slug'])  # case insensitive LIKE clause
        questions = Questions.objects.filter(quizz=quiz)
        serializer = QuestionSerializer(questions, many=True)  # add related name to the models for working
        return Response(serializer.data)

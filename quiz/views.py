from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from .models import Questions, Quizzer
from .serializers import QuizzerSerializer, QuestionSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView, Response

from django.shortcuts import get_object_or_404
from .forms import QuestionsFormset,QuizForm
from .filters import QuizFilter


def create_quiz_form(request):
    
    if request.method=='POST':
        ques_fromset=QuestionsFormset(request.POST)
        quiz_form=QuizForm(request.POST,request.FILES)
        if ques_fromset.is_valid() and quiz_form.is_valid():
            quiz_instance=quiz_form.save(commit=False)
            print('---atleast not reached her eright?')
            quiz_instance.save()
            quiz_form.save_m2m()
            instance = ques_fromset.save(commit=False)
            for i in instance:  

                i.quizz=quiz_instance        
            for i in instance:
                i.save()
            return redirect('/quizzes/')
    else:
        ques_fromset = QuestionsFormset()
        quiz_form=QuizForm()

    return render(request, 'quiz/create-quiz.html', {'quest_form': ques_fromset,'quiz_form':quiz_form})

def update_quiz_form(request, quizzer_id):
    inst=get_object_or_404(Quizzer,id=quizzer_id)
    if request.method=='POST':
        
        quiz_form=QuizForm(request.POST,request.FILES,instance=inst)
        ques_fromset=QuestionsFormset(request.POST,instance=inst)
        print('atleas i am here-------',ques_fromset.errors,quiz_form.is_valid())
        if ques_fromset.is_valid() and quiz_form.is_valid():
            
            quiz_instance=quiz_form.save(commit=False)
            quiz_instance.user=request.user
            quiz_instance.save()
            quiz_form.save_m2m()
            print('right over here-----------')
            instance = ques_fromset.save(commit=False)
            for i in instance:  
                i.quizz=quiz_instance        
            for i in instance:
                print('----and herer')
                i.save()
            return redirect('/quizzes/')
    else:
        ques_fromset = QuestionsFormset(instance=inst)
        quiz_form=QuizForm(instance=inst)

    return render(request, 'quiz/create-quiz.html', {'quest_form': ques_fromset,'quiz_form':quiz_form})

class QuizzView(DetailView):
    model = Quizzer
    fields = '__all__'
    template_name = 'quiz/quiz.html'



def Quizzes(request):
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

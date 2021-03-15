from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from .models import Questions, Quizzer
from .serializers import QuizzerSerializer, QuestionSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView, Response

from django.shortcuts import get_object_or_404
from django.forms.models import inlineformset_factory
from django.forms import ModelForm
QuestionsFormset = inlineformset_factory(Quizzer,Questions,fields=['question','option_1','option_2','option_3','option_4','answer'],extra=1)

class QuizForm(ModelForm):
    class Meta:
        model=Quizzer
        fields=['title','tags']
def create_quiz_form(request):
    ques_fromset=QuestionsFormset(request.POST or None)
    quiz_form=QuizForm(request.POST or None)
    if request.method=='POST' and ques_fromset.is_valid() and quiz_form.is_valid():
        quiz_instance=quiz_form.save(commit=False)
        quiz_instance.user=request.user
        quiz_instance.save()
        quiz_form.save_m2m()
        # title=request.POST['title']
        # x= Quizzer.objects.create(title=title,user=request.user)
        instance = ques_fromset.save(commit=False)
        print('-------over here----',quiz_instance,quiz_instance.title)
        for i in instance:  
            i.quizz=quiz_instance        
        for i in instance:
            i.save()
        return redirect('/quizzes/')
    else:
        ques_fromset = QuestionsFormset()

    return render(request, 'quiz/base.html', {'quest_form': ques_fromset,'quiz_form':quiz_form})

def update_quiz_form(request, quizzer_id=None):
    inst=get_object_or_404(Quizzer,id=quizzer_id)
    quiz_form=QuizForm(request.POST or None,instance=inst)
    # x = Quizzer.objects.get(id=quizzer_id)
    # title=x.title
    # print('--------------title over hererer-------',title)
    ques_fromset=QuestionsFormset(request.POST or None,instance=inst)
    if request.method=='POST' and ques_fromset.is_valid():
        instance = ques_fromset.save(commit=False)
        for i in instance:  
            i.quizz=inst        
        for i in instance:
            i.save()
        return redirect('/quizzes/')
    else:
        ques_fromset = QuestionsFormset(instance=inst)

    return render(request, 'quiz/base.html', {'form': ques_fromset,'quiz_form':quiz_form})

class QuizzView(DetailView):
    model = Quizzer
    fields = '__all__'
    template_name = 'quiz/quiz.html'

class QuizzesView(ListView):
    model = Quizzer
    context_object_name = 'quizzes'
    template_name = 'quiz/quizzes.html'


class QuizzesApiView(ListAPIView):
    serializer_class = QuizzerSerializer
    queryset = Quizzer.objects.all()


class QuizzApiView(APIView):
    def get(self, request, format=None, **kwargs):
        quiz = get_object_or_404(Quizzer, slug__iexact=kwargs['slug'])  # case insensitive LIKE clause
        questions = Questions.objects.filter(quizz=quiz)
        serializer = QuestionSerializer(questions, many=True)  # add related name to the models for working
        return Response(serializer.data)


# class QuizCreateView(CreateView):
#     template_name='quiz/base.html'

#     form_class=QuestionsFormset
#     success_url = '/quizzes/'
    
#     def form_valid(self, form,instance=None):
#         title=self.request.POST['title']
#         try:
#             x = Quizzer.objects.get(id=instance)
#         except:
#             x= Quizzer.objects.create(title=title,user=self.request.user)
#         instance = form.save(commit=False)
#         for i in instance:  
#             i.quizz=x        
#         for i in instance:
       
#             i.save()
  
#         # return super().form_valid(form)


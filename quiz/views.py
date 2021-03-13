from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from .models import Questions, Quizzer
from .serializers import QuizzerSerializer, QuestionSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView, Response

from django.shortcuts import get_object_or_404
from django.forms.models import inlineformset_factory

QuestionsFormset = inlineformset_factory(Quizzer,Questions,fields=['question','option_1','option_2','option_3','option_4','answer'],extra=1)
def create_quiz_form(request):
    formset=QuestionsFormset(request.POST or None)
    if request.method=='POST' and formset.is_valid():
        title=request.POST['title']
        x= Quizzer.objects.create(title=title,user=request.user)
        instance = formset.save(commit=False)
        for i in instance:  
            i.quizz=x        
        for i in instance:
            i.save()
        return redirect('/quizzes/')
    else:
        formset = QuestionsFormset()

    return render(request, 'quiz/base.html', {'form': formset})

def update_quiz_form(request, quizzer_id=None):
    x = Quizzer.objects.get(id=quizzer_id)
    title=x.title
    print('--------------title over hererer-------',title)
    formset=QuestionsFormset(request.POST or None,instance=x)
    if request.method=='POST' and formset.is_valid():
        instance = formset.save(commit=False)
        for i in instance:  
            i.quizz=x        
        for i in instance:
            i.save()
        return redirect('/quizzes/')
    else:
        formset = QuestionsFormset(instance=x)

    return render(request, 'quiz/base.html', {'form': formset,'title':title})

class QuizzView(DetailView):
    model = Quizzer
    fields = '__all__'
    template_name = 'quiz/quiz.html'

class QuizzesView(ListView):
    model = Quizzer
    context_object_name = 'quizzes'
    template_name = 'quiz/quizzes.html'


class QuizzesView(ListAPIView):
    serializer_class = QuizzerSerializer
    queryset = Quizzer.objects.all()


class QuizzView(APIView):
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


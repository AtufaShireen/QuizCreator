from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProfileUpdateForm, UserUpdateForm, UserRegsitrationForm
from django.contrib.auth.decorators import login_required
from quiz.models import Quizzer,QuizScore
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.http import Http404

def register(request):
    if request.user.is_authenticated:
        return redirect('quiz:quizzes')
    if request.method == 'POST':
        form = UserRegsitrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}')
            return redirect('profile')  
    else:
        form = UserRegsitrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request,view_user=None):
    if view_user is not None:
        try:
            user=User.objects.get(username=view_user)
        except User.DoesNotExist:
            messages.warning(request, f'User Doesnot Exists')
            raise Http404()        
        x = Quizzer.objects.filter(Q(user__username=view_user),Q(private=False))
        tags=x[0].user_tags()
        t=QuizScore.objects.filter(user=user)
        score=[(y.score,y.quiz) for y in t]
        context = {'quiz_score':score,'public':x,'author':False,'user':user,'tags_used':tags}
        return render(request, 'users/profile.html', context)

    private = Quizzer.objects.filter(Q(user=request.user),Q(private=True))
    public = Quizzer.objects.filter(Q(user=request.user),Q(private=False))
    try:
        tags=public[0].user_tags()
    except:
        tags=[]
    t=QuizScore.objects.filter(user=request.user)
    score=[(y.score,y.quiz) for y in t]
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():

            u_form.save()
            p_form.save()

            messages.success(request, 'Your Profile has been updated!')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

    context = {'u_form': u_form,'p_form': p_form,'quiz_score':score,'public':public,
                'private':private,'author':True,'tags_used':tags}
    return render(request, 'users/profile.html', context)

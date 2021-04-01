from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProfileUpdateForm, UserUpdateForm, UserRegsitrationForm
from django.contrib.auth.decorators import login_required
from quiz.models import Quizzer,QuizScore

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegsitrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}')
            return redirect('profile')  # change to blog-home
    else:
        form = UserRegsitrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request,view_user=None):
    if view_user is not None:
        print('user seelecteded------------',view_user)
        x = Quizzer.objects.filter(user__username=view_user)
        t=QuizScore.objects.filter(score__gte=1)
        score=[(y.score,y.quiz) for y in t]
        context = {'quiz_score':score,'created_quizzes':x,'author':False} #,'quizzes':x
        return render(request, 'users/profile.html', context)
    x = Quizzer.objects.filter(user=request.user)
    t=QuizScore.objects.filter(score__gte=1)
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

    context = {'u_form': u_form,'p_form': p_form,'quiz_score':score,'created_quizzes':x,'author':True} #,'quizzes':x
    return render(request, 'users/profile.html', context)

# def viewprofile(request,username):

#     context = {'quiz_score':score,'created_quizzes':x}
#     return render(request, 'users/profile.html', context)
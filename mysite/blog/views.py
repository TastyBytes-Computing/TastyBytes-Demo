from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from . import models
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm, ProfileForm

class HomeView(TemplateView):
    """views for the home.html"""
    template_name = "blog/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_posts = models.Post.objects.order_by('updated').reverse()
        context.update(
            {
                'latest_posts' : latest_posts
            }
        )
        return context

# signup page
def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'blog/signup.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username = username, password = password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect('login')

def profile(request):
    if request.user.is_authenticated:
        user_posts =models.Post.objects.filter(author=request.user)
        user_profile = models.Profile.objects.get(user = request.user)
        return render(request, 'blog/profile.html', {'user_posts': user_posts, 'user_profile': user_profile})
    else:
        return redirect('login')

def edit_profile(request):
    if request.user.is_authenticated:
        user_profile = models.Profile.objects.get(user = request.user)
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
                return redirect('edit_profile')
        else:
            form = ProfileForm(instance=user_profile)
        return render(request, 'blog/edit.html', {'form':form})
    else:
        return redirect('login')
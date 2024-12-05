from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm, UserRegisterForm
from .models import Game, User
from django.views import View
from django.contrib.auth.hashers import make_password

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')

class GameCollectionView(View):
    games = Game.objects.all()
    def get(self, request, *args, **kwargs):
        return render(request, 'games.html', {'games': self.games})

class UserRegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserRegisterForm
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
            )
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('register_complete')
        return render(request, 'register.html', {'form': form})

class UserRegisterCompleteView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register_complete.html')

class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        form = UserLoginForm
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'login.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, UserRegisterForm
from .models import Game, User
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')

class GameCollectionView(View):
    games = Game.objects.all()
    def get(self, request, *args, **kwargs):
        return render(request, 'games.html', {'games': self.games})

class UserRegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_complete')
        return render(request, 'register.html', {'form': form})

class UserRegisterCompleteView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register_complete.html')

class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            return redirect('home')
        return render(request, 'login.html', {'form': form})

class UserLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')

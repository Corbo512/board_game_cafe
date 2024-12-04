from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import UserModelForm
from .models import Game
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
        form = UserModelForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('register_complete')
        return render(request, 'register.html', {'form': form})

class UserRegisterCompleteView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register_complete.html')

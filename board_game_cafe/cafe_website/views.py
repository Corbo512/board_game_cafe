from django.shortcuts import render
from django.contrib.auth import authenticate
from .forms import UserLoginForm
from .models import Game
from django.views import View

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')

class GameCollectionView(View):
    games = Game.objects.all()
    def get(self, request, *args, **kwargs):
        return render(request, 'games.html', {'games': self.games})

class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': UserLoginForm()
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                raise "Username or password is incorrect"
            return render(request, 'login.html', context)

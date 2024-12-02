from django.shortcuts import render
from .models import Game
from django.views import View
from django.urls import reverse_lazy

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


class GameCollectionView(View):
    games = Game.objects.all()
    def get(self, request, *args, **kwargs):
        return render(request, 'games.html', {'games': self.games})

from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, UserRegisterForm, ReservationForm
from .models import Game, CustomUser, Reservation
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')

class GameCollectionView(ListView):
    model = Game
    template_name = 'games.html'
    context_object_name = 'games'
    paginate_by = 12
    ordering = ['name']

class UserRegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
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
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'form': form})

class UserLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')

class ReservationCreateView(CreateView):
    model = Reservation
    template_name = 'reservation.html'
    form_class = ReservationForm

    def get_initial(self):
        game_id = self.kwargs['game_id']
        game = get_object_or_404(Game, id=game_id)
        return {'game': game}

    def get_context_data(self):
        context = super().get_context_data()
        game_id = self.kwargs['game_id']
        context['game'] = get_object_or_404(Game, id=game_id)
        return context

class GameListView(ListView):
    model = Game
    template_name = 'games_for_reservation.html'
    context_object_name = 'games'
    paginate_by = 12
    ordering = ['name']

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, UserRegisterForm, ReservationForm
from .models import Game, Reservation
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import fetch_game_details

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
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form, 'next': request.GET.get('next', '/')})

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                next_url = request.POST.get('next', 'home')
                return redirect(next_url)
        return render(request, 'login.html', {'form': form})

class UserLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class ReservationCreateView(LoginRequiredMixin, CreateView):
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

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            existing_reservations = Reservation.objects.filter(
                game=reservation.game,
                start_time__date=reservation.start_time.date()
            ).order_by('start_time') | Reservation.objects.filter(
                table=reservation.table,
                start_time__date=reservation.start_time.date()
            ).order_by('start_time')

            for conflict in existing_reservations:
                if reservation.start_time < conflict.end_time and reservation.end_time > conflict.start_time:
                    if conflict.game == reservation.game:
                        form.add_error(None,
                                       f'{reservation.game} is already reserved from {conflict.start_time} to {conflict.end_time}')
                    if conflict.table == reservation.table:
                        form.add_error(None,
                                       f'{reservation.table} is already reserved from {conflict.start_time} to {conflict.end_time}')
                    return render(request, self.template_name,
                                  {'form': form, 'game': reservation.game, 'table': reservation.table})

            reservation.user = request.user
            reservation.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class GameListView(ListView):
    model = Game
    template_name = 'games_for_reservation.html'
    context_object_name = 'games'
    paginate_by = 12
    ordering = ['name']

class GameDetailsView(DetailView):
    model = Game
    template_name = 'game_details.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game_details = fetch_game_details('games.xml')
        game_name = self.object.name

        xml_game = ''
        for game in game_details:
            if game['title'] == game_name:
                xml_game = game
                break

        context['xml_game'] = xml_game
        return context

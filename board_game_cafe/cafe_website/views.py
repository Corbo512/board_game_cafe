from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import UserRegisterForm, ReservationForm
from .models import Game, Reservation
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(TemplateView):
    template_name = 'home.html'

class GameCollectionView(ListView):
    model = Game
    template_name = 'games.html'
    context_object_name = 'games'
    paginate_by = 12
    ordering = ['name']

class UserRegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('register_complete')

class UserRegisterCompleteView(TemplateView):
    template_name = 'register_complete.html'

class UserLoginView(LoginView):
    template_name = 'login.html'

class UserLogoutView(LogoutView):
    next_page = 'home'

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

            #optymalnie ustawić maks czas rezerwacji na 30 dni i od start_time odjąć 30
            existing_reservations = (Reservation.objects.filter(
                game=reservation.game).order_by('start_time') |
            Reservation.objects.filter(
                table=reservation.table).order_by('start_time'))

            reservation.user = request.user

            for conflict in existing_reservations:
                print(conflict)
                if reservation.start_time < conflict.end_time and reservation.end_time > conflict.start_time:
                    if conflict.game == reservation.game:
                        form.add_error(None,
                                       f'{reservation.game} is already reserved from {conflict.start_time} to {conflict.end_time}')
                    if conflict.table == reservation.table:
                        form.add_error(None,
                                       f'{reservation.table} is already reserved from {conflict.start_time} to {conflict.end_time}')
                    return render(request, self.template_name,
                                  {'form': form, 'game': reservation.game,
                                   'table': reservation.table})

            reservation.save()
            return redirect('reservation_complete')

        return render(request, self.template_name, {'form': form})

class ReservationCompleteView(TemplateView):
    template_name = 'reservation_complete.html'

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
        context['authors'] = self.object.author.all()
        return context

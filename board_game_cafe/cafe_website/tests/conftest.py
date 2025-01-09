import pytest
from django.contrib.auth import get_user_model

@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="password123")

@pytest.fixture
def game(db):
    from cafe_website.models import Game
    return Game.objects.create(name="Wingspan", description="bird enthusiasts")

@pytest.fixture
def table(db):
    from cafe_website.models import Table
    return Table.objects.create(number=1, capacity=4)

@pytest.fixture
def reservation(db, user):
    from cafe_website.models import Reservation, Game, Table

    game = Game.objects.create(name="Wingspan", description="bird enthusiasts")
    table = Table.objects.create(number=1, capacity=4)

    return Reservation.objects.create(
        user=user,
        game=game,
        table=table,
        start_time="2024-12-02 11:11:00+00:00",
        end_time="2024-12-04 11:11:00+00:00"
    )

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

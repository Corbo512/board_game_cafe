import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_game_collection_view(client):
    response = client.get(reverse('games'))
    assert response.status_code == 200
    assert "Our collection" in response.content.decode()

@pytest.mark.django_db
def test_game_details_view(client, game):
    response = client.get(reverse('game_details', args=[game.pk]))
    assert response.status_code == 200
    assert "Wingspan" in response.content.decode()
    assert "bird enthusiasts" in response.content.decode()

@pytest.mark.django_db
def test_user_login_view(client, user):
    response = client.post(reverse('login'), {"username": "testuser", "password": "password123"})
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_user_login_redirect_with_next(client, user):
    login_url = '/accounts/login/?next=/reservation/1/'
    response = client.post(login_url, {"username": "testuser", "password": "password123"})
    assert response.status_code == 302
    assert response.url == '/reservation/1/'

@pytest.mark.django_db
def test_user_login_invalid_credentials(client):
    response = client.post('/accounts/login/', {"username": "wronguser", "password": "wrongpassword"})
    assert response.status_code == 200
    assert "Please enter a correct username and password" in response.content.decode()

@pytest.mark.django_db
def test_user_logout_view(client, user):
    client.login(username="testuser", password="password123")
    response = client.post(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_user_register_view(client):
    url = reverse('register')
    register_data = {
        "username": "testuser",
        "email": "testemail@mail.com",
        "password1": "TESTpassword123",
        "password2": "TESTpassword123",
    }
    response = client.post(url, register_data)

    assert response.status_code == 302
    assert response.url == reverse('register_complete')

    User = get_user_model()
    assert User.objects.filter(username="testuser").exists()

@pytest.mark.django_db
def test_user_register_invalid_credentials(client):
    url = reverse('register')
    register_data = {
        "username": "testuser",
        "email": "testemail@mail.com",
        "password1": "123",
        "password2": "123",
    }
    response = client.post(url, register_data)

    assert response.status_code == 200

    User = get_user_model()
    assert not User.objects.filter(username="testuser").exists()

@pytest.mark.django_db
def test_user_logout_view(client, user):
    client.login(username="testuser", password="password123")
    response = client.post(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_reservation_create_view(client, user, game, table):
    client.login(username="testuser", password="password123")
    url = reverse('reservation', kwargs={'game_id': game.id})
    reservation_data = {
        "game": game.id,
        "table": table.id,
        "start_time": "2025-12-01 11:11:00+00:00",
        "end_time": "2025-12-02 11:11:00+00:00"
    }
    response = client.post(url, reservation_data)

    assert response.status_code == 302
    assert response.url == reverse('reservation_complete')

    from cafe_website.models import Reservation
    assert Reservation.objects.filter(user=user, game=game, table=table).exists()

@pytest.mark.django_db
def test_reservation_create_view_invalid_data(client, user, game, table, reservation):
    client.login(username="testuser", password="password123")
    url = reverse('reservation', kwargs={'game_id': game.id})
    reservation_data = {
        "game": game.id,
        "table": table.id,
        "start_time": "2024-12-01 11:11:00+00:00",
        "end_time": "2024-12-03 11:11:00+00:00"
    }
    response = client.post(url, reservation_data)

    assert response.status_code == 200


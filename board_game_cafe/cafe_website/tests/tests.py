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

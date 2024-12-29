"""
URL configuration for board_game_cafe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cafe_website.views import HomeView, GameCollectionView, UserRegisterView, UserRegisterCompleteView, UserLoginView, UserLogoutView, ReservationCreateView, GameListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('games/', GameCollectionView.as_view(), name='games'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('register-complete/', UserRegisterCompleteView.as_view(), name='register_complete'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('reservation/<int:game_id>/', ReservationCreateView.as_view(), name='reservation'),
    path('games_reservation/', GameListView.as_view(), name='games_reservation'),
]

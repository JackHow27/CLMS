from django.urls import path
from . import views
from .views import match_list

urlpatterns = [
    path('', views.home, name='home'),
    path('teams/', views.teams, name='teams'),
    path('players/', views.players, name='players'),
    path('matches/', views.match_list, name='matches'),
    path('match/<int:pk>/', views.MatchDetailView.as_view(), name='match_detail'),
]
from django.urls import include, path
from . import views
from .views import match_list
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('teams/', views.teams, name='teams'),
    path('players/', views.players, name='players'),
    path('matches/', views.match_list, name='matches'),
    path('match/<int:pk>/', views.MatchDetailView.as_view(), name='match_detail'),

    path('players/login/', auth_views.LoginView.as_view(), name='login'),
    path('players/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('players/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('players/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('players/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('players/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

from django.urls import path
from . import views
from .views import match_list, register
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('teams/', views.teams, name='teams'),
    path('players/', views.players, name='players'),
    path('matches/', views.match_list, name='matches'),
    path('match/<int:pk>/', views.MatchDetailView.as_view(), name='match_detail'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('calendar/', views.calendar, name='calendar'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

]
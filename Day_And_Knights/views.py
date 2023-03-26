from django.shortcuts import render
from .models import Match, Player, Team

def home(request):
    return render(request, 'home.html')

def match_list(request):
    matches = Match.objects.all()
    return render(request, 'match_list.html', {'matches': matches})

def index(request):
    return render(request, 'index.html')

def teams(request):
    Teams = Team.objects.all
    return render(request, 'teams.html', {'teams': Teams})

def players(request):
    Players = Player.objects.all()
    return render(request, 'players.html', {'players': Players})

def results(request):
    return render(request, 'results.html')


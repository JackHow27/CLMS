from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import Match, Player, Team, League
from django.contrib.auth.decorators import login_required
from .forms import PlayerRegistrationForm

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

class MatchDetailView(View):
    template_name = 'match.html'

    def get(self, request, pk):
        match = get_object_or_404(Match, pk=pk)
        context = {'match': match}
        return render(request, self.template_name, context)

def register(request):
    if request.method == 'POST':
        form = PlayerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            player = Player(user=user, first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], phone_number=form.cleaned_data['phone_number'], email=form.cleaned_data['email'], ecf_code=form.cleaned_data['ecf_code'])
            player.save()
            return redirect('home')
    else:
        form = PlayerRegistrationForm()
    return render(request, 'register.html', {'form': form})

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'login.html')

def calendar(request):
    return render(request, 'calendar.html')

def league_list(request):
    leagues = League.objects.all()
    return render(request, 'league_list.html', {'leagues': leagues})

class league(View):
    template_name = 'league.html'

    def get(self, request, pk):
        league = get_object_or_404(League, pk=pk)
        context = {'league': league}
        return render(request, self.template_name, context)
    
def test(request):
    return render(request, 'test.html')



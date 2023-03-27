import requests
import json
import datetime
import uuid
from datetime import date
from django.db import models
from types import SimpleNamespace
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password, check_password


class Player(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    ecf_code = models.CharField(max_length=200)
    username = models.CharField(default=uuid.uuid4().hex, max_length=150, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    ecf_rating = models.IntegerField(blank=True, null=True)
     
    def get_ecf_rating(self):
        if(self.ecf_code):
            url = f'https://www.ecfrating.org.uk/v2/new/api.php?v2/ratings/S/{self.ecf_code}/{date.today().isoformat()}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') == True:
                    return data.get('original_rating')
            return None
        return None
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_teams_display(self):
        return ', '.join([team.team_name for team in self.teams.all()])
    
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.generate_username()
        self.ecf_rating = self.get_ecf_rating()
        super(Player, self).save(*args, **kwargs)

    def generate_username(self):
        username = f"{self.first_name.lower()}.{self.last_name.lower()}".replace(" ", "")
        count = Player.objects.filter(username__startswith=username).count()
        if count == 0:
            return username
        else:
            return f"{username}{count+1}"
        
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    


    
class League(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    boards_per_match = models.IntegerField(default=6)
    active = models.BooleanField(default=False)
    day_to_play = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ], default='Wednesday')


    

    def __str__(self):
        return self.name
    
    def get_teams(self):
        return self.teams.all()

    def save(self, *args, **kwargs):        
        from .utils import generate_matches, create_boards_for_league
        super().save(*args, **kwargs)
        teams = self.get_teams()
        generate_matches(self)
        create_boards_for_league(self)
    
class Team(models.Model):
    team_name = models.CharField(max_length=200)
    team_logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)
    description = models.TextField()
    home_field = models.CharField(max_length=50)
    home_address = models.CharField(max_length=100)
    captain = models.OneToOneField(Player, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player, related_name='teams')
    rank = models.IntegerField(default=0)
    League = models.ManyToManyField(League, related_name='teams')


    def __str__(self):
        return self.team_name


class Board(models.Model):
    match = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='boards')
    board_number = models.IntegerField()
    white_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='white_boards',blank=True,null=True)
    black_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='black_boards',blank=True,null=True)
    result = models.CharField(max_length=10, choices=[('1-0', '1-0'), ('0-1', '0-1'), ('1/2-1/2', '1/2-1/2'), ('*', '*')], blank=True)
    result_reason = models.TextField(blank=True)

    def __str__(self):
        return f"Board {self.board_number}: {self.result} ({self.match.home_team} vs. {self.match.away_team})"
    
    def exists(self):
        return Board.objects.filter(match=self.match, board_number=self.board_number).exists()

class Match(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='matches')
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    result = models.CharField(max_length=20, blank=True)



    def numeric_result(self, player):
        boards = self.boards.all()
        score = 0
        for board in boards:
            if board.result == "1-0" and board.white_player == player:
                score += 1
            elif board.result == "0-1" and board.black_player == player:
                score += 1
            elif board.result == "1/2-1/2":
                score += 0.5
        return score

    def set_results(self):
        home_team = self.home_team
        away_team = self.away_team

        home_score = 0
        away_score = 0

        for player in home_team.players.all():
            home_score += self.numeric_result(player)

        for player in away_team.players.all():
            away_score += self.numeric_result(player)

        self.result = f"{home_score} - {away_score}"

        
    def __str__(self):
        return f'{self.home_team} vs. {self.away_team}'
    
    def save(self, *args, **kwargs):
        if not self.location:
            self.location = self.home_team.home_field
        super(Match, self).save(*args, **kwargs)
        self.set_results()



    class Meta:
        ordering = ('date', 'time',)
    
    class Meta:
        verbose_name_plural = "matches"



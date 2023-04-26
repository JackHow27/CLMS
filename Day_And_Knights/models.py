import requests
import json
import datetime
from datetime import date
from django.db import models
from types import SimpleNamespace
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    ecf_code = models.CharField(max_length=200)
     
    def get_ecf_rating(self):
        url = f'https://www.ecfrating.org.uk/v2/new/list_player.php?code={self.ecf_code}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK':
                return data.get('rating')
        return None
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_teams_display(self):
        return ', '.join([team.team_name for team in self.teams.all()])
    
    def name(self):
        return f"{self.first_name} {self.last_name}"

    
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
    
    @property
    def teams_count(self):
        return self.get_teams().count()

    def save(self, *args, **kwargs):        
        from .utils import generate_matches, create_boards_for_league
        super().save(*args, **kwargs)
        teams = self.get_teams()
        generate_matches(self)
        create_boards_for_league(self)
    
class Team(models.Model):
    team_name = models.CharField(max_length=200)
    team_logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    home_field = models.CharField(max_length=50, blank=True, null=True)
    home_address = models.CharField(max_length=100, blank=True, null=True)
    captain = models.OneToOneField(Player, on_delete=models.CASCADE, blank=True, null=True)
    players = models.ManyToManyField(Player, related_name='teams', blank=True, null=True)
    rank = models.IntegerField(default=0, blank=True, null=True)
    League = models.ManyToManyField(League, related_name='teams')


    def __str__(self):
        return self.team_name

class Board(models.Model):
    #match = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='boards')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
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
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    boards = models.ManyToManyField(Board)
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

        self.home_score = home_score
        self.away_score = away_score
        self.result = f"{home_team.team_name}:{home_score} - {away_team.team_name}:{away_score}"

        
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

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    no_sections = models.IntegerField()
    format = models.CharField(max_length=50, choices=[
        ('Swiss', 'Swiss'),
        ('Round Robin', 'Round Robin'),
        #('Single Elimination', 'Single Elimination'),
        #('Double Elimination', 'Double Elimination')
    ])
    #double_elimination_bracket_reset = models.BooleanField(default=True)
    active = models.BooleanField(default=False)
    timeformat = models.IntegerField()
    increment = models.IntegerField(default=0)
    round_format = models.CharField(max_length=50,default='Single Game', choices=[
        ('Single Game','Single Game'),
        ('Best of 3', 'Best of 3')
    ])


class Section():
    Tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='Section')
    name = models.CharField(max_length=100, default='All')
    no_rounds = models.IntegerField(null=True, default=0, blank=True)
    players = models.ManyToManyField(Player)
    current_round = models.PositiveIntegerField(default=1)


class Round():
    section = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='round')
    datetime = models.DateTimeField(blank=True, null=True)
    round_number = models.IntegerField()
    boards = models.ManyToManyField(Board)






from django.core.management.base import BaseCommand
import random
from datetime import timedelta, datetime
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Website.settings")
django.setup()

from Day_And_Knights.models import League, Team, Player

class Command(BaseCommand):
    help = 'Create leagues'

    def handle(self, *args, **options):
        LEAGUE_FILE = os.path.join(os.path.dirname(__file__), 'test-data', 'leagues.txt')
        print(LEAGUE_FILE)
        with open(LEAGUE_FILE, 'r') as f:
            leagues = f.read().splitlines()
    
        print(f"Number of leagues: {len(leagues)}")
        for league_name in random.sample(leagues, 5):
            league = League(name=league_name,start_date=datetime.now(), end_date=datetime.now() + timedelta(days=365), boards_per_match=random.choice([1,2,3,4,5,6,7,8,9,10]))
            league.save()

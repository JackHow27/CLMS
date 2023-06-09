from Day_And_Knights.models import Match, Board, Tournament, Section, Round
from django.core.exceptions import ObjectDoesNotExist
import datetime



def schedule_league_matches(league):
    # Generate match dates for the league
    match_dates = generate_match_dates(league.day_to_play, league.start_date, league.end_date)

    # Tuple list to keep track of what teams have played on what day 
    teams_playing_on_day = [(),()]

    # Loop through each match and find a date for it
    for match in league.matches.all():
        # Create a list of teams that are already scheduled to play on the same day
        
        
        # Loop through each match date until a suitable one is found
        for date in match_dates:
            # Check if either team is already scheduled to play on this date
            if (match.home_team, date) in teams_playing_on_day or (match.away_team, date) in teams_playing_on_day:
                continue
            
            # Create the match on this date
            match.date = date
            match.save()
            
            # Add the teams to the list of teams playing on this day
            teams_playing_on_day.append((match.home_team, date))
            teams_playing_on_day.append((match.away_team, date))
            
            # Exit the loop once a date has been found for this match
            break



def generate_match_dates(day_to_play, start_date, end_date):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_index = days.index(day_to_play)
    delta = day_index - start_date.weekday() if day_index >= start_date.weekday() else (7 - start_date.weekday() + day_index)
    date = start_date + datetime.timedelta(days=delta)
    match_dates = []
    while date <= end_date:
        match_dates.append(date)
        date += datetime.timedelta(days=7)
    return match_dates

def find_match_date(team1, team2, match_dates, matches):
    for date in match_dates:

        # check if both teams are available on the date
        if team1 not in [match.home_team or match.away_team for match in matches if match.date == date] and \
           team2 not in [match.home_team or match.away_team for match in matches if match.date == date]:
            return date
    
    return None

def generate_matches(league):
    teams = list(league.teams.all())
    num_teams = len(teams)

    if num_teams % 2 == 1:
        teams.append(None)
        num_teams += 1

    matches = []

    for i in range(num_teams - 1):
        for j in range(i+1, num_teams):
            home_team = teams[i]
            away_team = teams[j]

            if home_team is None or away_team is None:
                continue

            home_matches = [match for match in matches if match.home_team == home_team]
            away_matches = [match for match in matches if match.away_team == home_team]

            for match_num in range(2):
                if match_num == 0:
                    # Home match
                    match = Match.objects.create(
                        league=league,
                        home_team=home_team,
                        away_team=away_team
                    )
                    matches.append(match)
                else:
                    # Away match
                    match = Match.objects.create(
                        league=league,
                        home_team=away_team,
                        away_team=home_team
                        )
                    matches.append(match)

    schedule_league_matches(league)

    return matches



def match_exists(team1, team2):
    try:
        match = Match.objects.get(home_team=team1, away_team=team2)
        return True
    except ObjectDoesNotExist:
        return False

def create_boards_for_league(league):
    for match in league.matches.all():
        for board_number in range(1, league.boards_per_match + 1):
            if not Board.objects.filter(match=match, board_number=board_number).exists():
                Board.objects.create(match=match, board_number=board_number)

def create_tournament_sections(tournament):
    for i in range(tournament.no_sections):
        Section.objects.create(Tournament=tournament, name=i)


def create_section_rounds(section):

    players = section.players.all()
    num_players = len(players)

    if num_players % 2 == 1:
        players.append(None)
        num_players += 1

    if section.Tournament.format == 'Swiss':
        i == 1 
        for i in range(section.no_rounds):
            round = Round.object.create(section=section, round_number=i)
            create_round_boards(round, players)
        return
    elif section.Tournament.format == 'Round Robin':
        for i in range(num_players - 1):
            round = Round.object.create(section=section, round_number=i)
            create_round_boards(round, players)
        return
    #elif section.Tournament.format == 'Single Elimination':
    #    for i in range(num_players / 2):
    #        round = Round.object.create(section=section, round_number=i)
    #        create_round_boards(round, players)
    #    return
    #elif section.Tournamnet.format == 'Double Elimination':
    #    number_of_rounds = num_players / 2
    #    if section.Tournament.double_elimination_bracket_reset:
    #        number_of_rounds += 1
    #    
    #    for i in range(num_players / 2):
    #        round = Round.object.create(section=section, round_number=i)
    #        create_round_boards(round, players)
    #    return
    
#WIP
def create_round_boards(round, players):
    num_players = len(players)
    if round.section.Tournament.format == 'Swiss':
        for i in range(num_players / 2 + 1):
                boards += Board.objects.create(content_type=Round, object_id=round.id, content_object=round)
                set_round_boards(boards, round, players)
        return
    elif round.section.Tournament.format == 'Round Robin':
        for i in range(num_players / 2 + 1):
                boards += Board.objects.create(content_type=Round, object_id=round.id, content_object=round)
                set_round_boards(boards, round, players)
        return
 # elif round.section.Tournament.format == 'Single Elimination':
 #     for i in range(num_players / (2 * round.round_number)):
 #             boards += Board.objects.create(content_type=Round, object_id=round.id, content_object=round)
 #             set_round_boards(boards, round, players)
 #     return
 # elif round.section.Tournamnet.format == 'Double Elimination':
 #     for i in range(num_players / (2 * (round.round_number - 1))):
 #             boards += Board.objects.create(content_type=Round, object_id=round.id, content_object=round)
 #             set_round_boards(boards, round, players)
 #     return
    return

def set_round_boards(boards, round, players):
    if round.section.Tournament.format == 'Swiss':
        if round.round_number == 1:
            #Set boards according to get_ecf_rating
            #Set Bye to bottom board
            return
        else:
            #Set boards according to current score
            #Set Bye to bottom board
            return
        
    elif round.section.Tournament.format == 'Round Robin':

       return
 #  elif round.section.Tournament.format == 'Single Elimination':

 #      return
 #  elif round.section.Tournamnet.format == 'Double Elimination':

 #      return
    return
    
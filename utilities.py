from datetime import datetime
from pprint import pprint

import requests
from fuzzywuzzy import fuzz

from models.FootballAPI import MatchAPI
from models.League import League

leagues = [
    # {"league": "La liga", "api_key": "soccer_spain_la_liga", "api_id": 2014},
    # {"league": "Premier League", "api_key": "soccer_england_league1", "api_id": 2021},
    # {"league": "Bundesliga", "api_key": "soccer_germany_bundesliga", "api_id": 2002},
    League(**{"league": "Serie A", "api_key": "soccer_italy_serie_a", "api_id": 2019})
]


def get_api_odds_teams(ligue: str):
    API_KEY = '1c4d52bcc762be6253526a6cb2179978'
    url = f"https://api.the-odds-api.com/v4/sports/{ligue}/participants?apiKey={API_KEY}"

    response = requests.request("GET", url)
    return [{'team_name': team['full_name'], 'team_ligue': ligue} for team in response.json()]


def get_api_football_teams(ligue_id: int):
    url = f"https://api.football-data.org/v4/competitions/{ligue_id}/teams?season=2024"

    headers = {
        'X-Auth-Token': '842e19d260114497a718642c69858dfa'
    }
    response = requests.request("GET", url, headers=headers)
    return [
        {'team_name': team['name'],
         'short_name': team['shortName'],
         'team_ligue': response.json()['competition']['name']}
        for team in response.json()['teams']
    ]


def create_mapping_table(leagues: list[League]):
    mapping_table = {}
    for league in leagues:
        odds_teams = get_api_odds_teams(league.api_key)
        football_teams = get_api_football_teams(league.api_id)
        for odds_team in odds_teams:
            best_match = None
            highest_ratio = 0
            for football_team in football_teams:
                # Comparaison avec le nom complet
                ratio_full = fuzz.ratio(odds_team['team_name'].lower(), football_team['team_name'].lower())
                # Comparaison avec le nom abrégé
                ratio_short = fuzz.ratio(odds_team['team_name'].lower(), football_team['short_name'].lower())
                # Sélection du meilleur ratio
                if ratio_full > highest_ratio:
                    highest_ratio = ratio_full
                    best_match = football_team
                if ratio_short > highest_ratio:
                    highest_ratio = ratio_short
                    best_match = football_team
            if highest_ratio > 70:
                mapping_table[odds_team['team_name']] = best_match['team_name']
    return mapping_table


def get_history_data(teams_id: str):
    url = f"https://api.football-data.org/v4/teams/{teams_id}/matches?status=FINISHED"

    headers = {
        'X-Auth-Token': '842e19d260114497a718642c69858dfa'
    }

    response = requests.request("GET", url, headers=headers)
    last_five_matches = \
        sorted(response.json()['matches'], key=lambda x: datetime.strptime(x['utcDate'], '%Y-%m-%dT%H:%M:%S%z'),
               reverse=True)[:5]
    return last_five_matches


if __name__ == "__main__":
    # data = get_history_data('78')
    # pprint(data[0])
    pprint(MatchAPI.summary('78'))
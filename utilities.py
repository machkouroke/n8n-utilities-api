import json
from datetime import datetime
from pprint import pprint

import requests
from fuzzywuzzy import fuzz

from models.League import League


def get_api_odds_teams(ligue: str):
    """
    Get the list of teams from the odds API `https://the-odds-api.com/account/`
    :param ligue: the id of the ligue in the odds API
    :return: the list of teams in the liguue on the odds API
    """
    API_KEY = '1c4d52bcc762be6253526a6cb2179978'
    url = f"https://api.the-odds-api.com/v4/sports/{ligue}/participants?apiKey={API_KEY}"

    response = requests.request("GET", url)
    return [{'team_name': team['full_name'], 'team_ligue': ligue} for team in response.json()]


def get_api_football_teams_free(ligue_id: int):
    """
    Get the list of teams from the football API `https://www.football-data.org/`
    :param ligue_id:  the id of the ligue in the football API
    :return:  the list of teams in the ligue on the football API
    """
    url = f"https://api.football-data.org/v4/competitions/{ligue_id}/teams?season=2024"

    headers = {
        'X-Auth-Token': '842e19d260114497a718642c69858dfa'
    }
    response = requests.request("GET", url, headers=headers)
    return [
        {'id': int(team['id']),
         'team_name': team['name'],
         'short_name': team['shortName'],
         'team_ligue': response.json()['competition']['name']}
        for team in response.json()['teams']
    ]








def get_fixture(home_team_id: int, away_team_id: int) -> int:
    """
    Get the fixture's id of the match between the home team and the away team
    :param home_team_id: the id of the home team
    :param away_team_id: the id of the away team
    :return: the fixture's id of the match
    """
    url = (f"https://v3.football.api-sports.io"
           f"/fixtures/headtohead?h2h={home_team_id}-{away_team_id}&date={datetime.now().strftime('%Y-%m-%d')}")
    headers = {
        'x-rapidapi-key': 'dde76b3c11fa752b6e09335d54e072c5',
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()['response'][0]['fixture']['id']


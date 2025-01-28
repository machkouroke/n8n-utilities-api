import json
from datetime import datetime
from pprint import pprint

import requests
from fuzzywuzzy import fuzz

from models.FootballAPI import MatchAPI
from models.League import League


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
        {'id': int(team['id']),
            'team_name': team['name'],
         'short_name': team['shortName'],
         'team_ligue': response.json()['competition']['name']}
        for team in response.json()['teams']
    ]


def create_mapping_table_odds_to_footapifree(leagues: list[League]):
    mapping_table = {}
    for league in leagues:
        odds_teams = get_api_odds_teams(league.odds_api_id)
        football_teams = get_api_football_teams(league.foot_api_free_id)
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


def create_mapping_table_footapifree_to_footapipaid(leagues: list[League]):
    foot_api_paid_teams = json.load(open('data/filtered_teams.json', encoding='utf-8'))
    mapping_table = {}
    for league in leagues:
        foot_api_free_teams = get_api_football_teams(league.foot_api_free_id)
        foot_api_paid_team_ligues = list(filter(lambda x: x['Country'] == league.foot_api_paid_name, foot_api_paid_teams))
        for foot_api_free_team in foot_api_free_teams:
            best_match = None
            highest_ratio = 0
            for foot_api_paid_team_ligue in foot_api_paid_team_ligues:
                foot_api_paid_team_ligue_name = foot_api_paid_team_ligue['Name'].lower()
                # Comparaison avec le nom complet
                ratio_full = fuzz.ratio(foot_api_paid_team_ligue_name, foot_api_free_team['team_name'].lower())
                # Comparaison avec le nom abrégé
                ratio_short = fuzz.ratio(foot_api_paid_team_ligue_name, foot_api_free_team['short_name'].lower())
                if ratio_full > highest_ratio:
                    highest_ratio = ratio_full
                    best_match = foot_api_paid_team_ligue
                if ratio_short > highest_ratio:
                    highest_ratio = ratio_short
                    best_match = foot_api_paid_team_ligue
            if highest_ratio >= 40:
                mapping_table[foot_api_free_team['id']] = best_match['ID']

    return mapping_table


def get_history_data(teams_id: str) -> list[dict]:
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
    leagues = [
        League(**{"name": "La liga", "odds_api_id":
            "soccer_spain_la_liga",
                  "foot_api_free_id": 2014,

                  "foot_api_paid_name": "Spain"
                  }),
        League(**{"name": "Premier League",
                  "foot_api_paid_name": "England",
                  "odds_api_id": "soccer_england_league1", "foot_api_free_id": 2021}),
        League(**{"name": "Bundesliga", "odds_api_id": "soccer_germany_bundesliga",
                  "foot_api_paid_name": "Germany",
                  "foot_api_free_id": 2002}),
        League(**{"name": "Serie A", "odds_api_id": "soccer_italy_serie_a", "foot_api_free_id": 2019,
                  "foot_api_paid_name": "Italy"}),
        League(**{"name": "Ligue 1", "odds_api_id": "soccer_france_ligue_one", "foot_api_free_id": 2015,
                  "foot_api_paid_name": "France"}),
    ]
    # old = {'Spain': 20, 'England': 20, 'Germany': 18, 'Italy': 20, 'France': 18}
    test = create_mapping_table_odds_to_footapipaid(
        leagues)
    # pprint(test)
    # print(len(test))
    # Get repartition of test by country size
    # countries = {}
    # for team in test:
    #     country = test[team]['team_name']['Country']
    #     if country not in countries:
    #         countries[country] = []
    #     countries[country].append(team)
    # # size of each country
    # for country in countries:
    #     print(f"{country}: {len(countries[country])}")
    # # Display for each country the team that are in the get_api_football_teams response but not in the mapping_table
    pprint(test)





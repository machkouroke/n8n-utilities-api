import enum
import json
from datetime import datetime
from pprint import pprint
from typing import Optional

import requests
from fuzzywuzzy import fuzz
from pydantic import BaseModel

from models.League import League
from utilities import get_api_odds_teams, get_api_football_teams_free


class Form(enum.Enum):
    W = "W"
    D = "D"
    L = "L"


class Outcome(BaseModel):
    name: str
    price: float


class Market(BaseModel):
    key: str
    last_update: datetime
    outcomes: list[Outcome]


class Bookmaker(BaseModel):
    key: str
    title: str
    last_update: datetime
    markets: list[Market]


class PredictionPercent(BaseModel):
    home: float
    draw: float
    away: float


class PredictionWinner(BaseModel):
    name: str
    comment: str


class Goal(BaseModel):
    total: float
    average: float


class Last5Matches(BaseModel):
    att: float
    defn: float
    conceded_goal: Goal
    scored_goal: Goal


class Repartition(BaseModel):
    home: float
    away: float
    total: float


class CompetitionTeamStat(BaseModel):
    form: list[Form]
    played: Repartition
    wins: Repartition
    draws: Repartition
    loses: Repartition
    total_scored_goal: Repartition
    total_conceded_goal: Repartition
    average_scored_goal: Repartition
    average_conceded_goal: Repartition


class TeamStat(BaseModel):
    last_5_matches_all_competitions: Last5Matches
    actual_competition_stat: CompetitionTeamStat


class Match(BaseModel):
    id: str
    home_team: str
    away_team: str
    bookmakers: list[Bookmaker]
    prediction: Optional[dict] = None

    @staticmethod
    def convert_percent_to_float(percent: str) -> float:
        return float(percent.replace('%', '')) / 100

    @staticmethod
    def create_mapping_table_odds_to_foot_api_paid(leagues: list[League]) -> dict[str, int]:
        """
        Create a mapping table between the teams of the odds API and the football API
        :param leagues:  the list of leagues to compare
        :return: the mapping table
        """
        foot_api_paid_teams = json.load(open('./data/filtered_teams.json', encoding='utf-8'))
        mapping_table = {}
        for league in leagues:
            odds_teams = get_api_odds_teams(league.odds_api_id)
            foot_api_paid_team_ligues = list(
                filter(lambda x: x['Country'] == league.foot_api_paid_name, foot_api_paid_teams))
            for foot_api_paid_team_ligue in foot_api_paid_team_ligues:
                foot_api_paid_team_ligue_name = foot_api_paid_team_ligue['Name'].lower()
                best_match = None
                highest_ratio = 0
                for odds_team in odds_teams:
                    # Comparaison avec le nom complet
                    ratio = fuzz.ratio(foot_api_paid_team_ligue_name, odds_team['team_name'].lower())
                    # Sélection du meilleur ratio
                    if ratio > highest_ratio:
                        highest_ratio = ratio
                        best_match = odds_team

                if highest_ratio > 60:
                    mapping_table[foot_api_paid_team_ligue['ID']] = best_match['team_name']

        return {v: k for k, v in mapping_table.items()}

    def get_odd_to_foot_api_paid_id(self, mapping_table_odd_to_paid: dict[str, int],) -> dict[str, int]:
        return {
            "home_team_id": mapping_table_odd_to_paid[self.home_team],
            "away_team_id": mapping_table_odd_to_paid[self.away_team]
        }

    def get_fixture(self, mapping_table_odd_to_paid: dict[str, int]) -> int:
        """
        Get the fixture's id of the match between the home team and the away team
        :param mapping_table_odd_to_paid:

        :return: the fixture's id of the match
        """
        team_id = self.get_odd_to_foot_api_paid_id(mapping_table_odd_to_paid)
        url = (f"https://v3.football.api-sports.io"
               f"/fixtures/headtohead?h2h={team_id['home_team_id']}-"
               f"{team_id['away_team_id']}&date={datetime.now().strftime('%Y-%m-%d')}")
        headers = {
            'x-rapidapi-key': 'dde76b3c11fa752b6e09335d54e072c5',
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        response = requests.request("GET", url, headers=headers)
        if not response.json()['response']:
            return -1
        return response.json()['response'][0]['fixture']['id']

    def set_prediction(self, fixture_id: int) -> None:
        url = f"https://v3.football.api-sports.io/predictions?fixture={fixture_id}"
        headers = {
            'x-rapidapi-key': 'dde76b3c11fa752b6e09335d54e072c5',
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        response = requests.request("GET", url, headers=headers)
        self.prediction = response.json()['response'][0]


if __name__ == "__main__":
    # data = get_history_data('78')
    # pprint(data[0])
    leagues = [
        League(**{"name": "La liga", "odds_api_id": "soccer_spain_la_liga",
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
    match = [
        {
            "id": "34b834fcc1c0e0a2284d7b6c05df975d",
            "home_team": "Leganés",
            "away_team": "Rayo Vallecano",
            "bookmakers": [
                {
                    "key": "pinnacle",
                    "title": "Pinnacle",
                    "last_update": "2025-01-29T22:32:56Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:56Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3.08
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.63
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.05
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "onexbet",
                    "title": "1xBet",
                    "last_update": "2025-01-29T22:32:56Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:56Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3.14
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.67
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.1
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "betclic",
                    "title": "Betclic",
                    "last_update": "2025-01-29T22:33:10Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:33:10Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3.02
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.52
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.02
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "marathonbet",
                    "title": "Marathon Bet",
                    "last_update": "2025-01-29T22:32:57Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:57Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3.05
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.59
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.02
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "tipico_de",
                    "title": "Tipico",
                    "last_update": "2025-01-29T22:32:59Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:59Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.55
                                },
                                {
                                    "name": "Draw",
                                    "price": 3
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "williamhill",
                    "title": "William Hill",
                    "last_update": "2025-01-29T22:32:57Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:57Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.6
                                },
                                {
                                    "name": "Draw",
                                    "price": 2.9
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "nordicbet",
                    "title": "Nordic Bet",
                    "last_update": "2025-01-29T22:32:57Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:57Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3.1
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.6
                                },
                                {
                                    "name": "Draw",
                                    "price": 3
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "betsson",
                    "title": "Betsson",
                    "last_update": "2025-01-29T22:32:58Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:58Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3.1
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.6
                                },
                                {
                                    "name": "Draw",
                                    "price": 3
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "suprabets",
                    "title": "Suprabets",
                    "last_update": "2025-01-29T22:28:46Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:28:46Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3.09
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.64
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.06
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "betfair_ex_eu",
                    "title": "Betfair",
                    "last_update": "2025-01-29T22:33:01Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:33:01Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3.25
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.7
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.05
                                }
                            ]
                        },
                        {
                            "key": "h2h_lay",
                            "last_update": "2025-01-29T22:33:01Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3.3
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.74
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.1
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "unibet_eu",
                    "title": "Unibet",
                    "last_update": "2025-01-29T22:32:57Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:57Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.63
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.1
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "everygame",
                    "title": "Everygame",
                    "last_update": "2025-01-29T22:31:30Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:31:30Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 2.95
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.55
                                },
                                {
                                    "name": "Draw",
                                    "price": 2.95
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "matchbook",
                    "title": "Matchbook",
                    "last_update": "2025-01-29T22:33:00Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:33:00Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3.25
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.7
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.05
                                }
                            ]
                        },
                        {
                            "key": "h2h_lay",
                            "last_update": "2025-01-29T22:33:00Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3.3
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.74
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.1
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "betonlineag",
                    "title": "BetOnline.ag",
                    "last_update": "2025-01-29T22:31:28Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:31:28Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3.08
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.63
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.03
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "coolbet",
                    "title": "Coolbet",
                    "last_update": "2025-01-29T22:32:58Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:58Z",
                            "outcomes": [
                                {
                                    "name": "Leganés",
                                    "price": 3.05
                                },
                                {
                                    "name": "Rayo Vallecano",
                                    "price": 2.7
                                },
                                {
                                    "name": "Draw",
                                    "price": 3
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "id": "efa06a0f691e9c3643845f4402a8aac4",
            "home_team": "Werder Bremen",
            "away_team": "FSV Mainz 05",
            "bookmakers": [
                {
                    "key": "tipico_de",
                    "title": "Tipico",
                    "last_update": "2025-01-29T22:32:21Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:21Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 2.9
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.4
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.4
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "onexbet",
                    "title": "1xBet",
                    "last_update": "2025-01-29T22:32:19Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:19Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 2.87
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.51
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.72
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "betclic",
                    "title": "Betclic",
                    "last_update": "2025-01-29T22:32:36Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:36Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 2.84
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.4
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.43
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "marathonbet",
                    "title": "Marathon Bet",
                    "last_update": "2025-01-29T22:32:20Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:20Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 2.79
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.44
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.62
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "betfair_ex_eu",
                    "title": "Betfair",
                    "last_update": "2025-01-29T22:32:21Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:21Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 2.96
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.56
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.55
                                }
                            ]
                        },
                        {
                            "key": "h2h_lay",
                            "last_update": "2025-01-29T22:32:21Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 3.05
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.62
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.6
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "pinnacle",
                    "title": "Pinnacle",
                    "last_update": "2025-01-29T22:32:19Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:19Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 2.92
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.53
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.38
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "williamhill",
                    "title": "William Hill",
                    "last_update": "2025-01-29T22:32:19Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:19Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 2.8
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.45
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.5
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "betsson",
                    "title": "Betsson",
                    "last_update": "2025-01-29T22:32:20Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:20Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 2.9
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.5
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.4
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "nordicbet",
                    "title": "Nordic Bet",
                    "last_update": "2025-01-29T22:30:55Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:30:55Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 2.9
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.5
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.4
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "unibet_eu",
                    "title": "Unibet",
                    "last_update": "2025-01-29T22:32:20Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:20Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 2.95
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.48
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.5
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "suprabets",
                    "title": "Suprabets",
                    "last_update": "2025-01-29T22:29:32Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:29:32Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 2.95
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.55
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.45
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "coolbet",
                    "title": "Coolbet",
                    "last_update": "2025-01-29T22:32:21Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:21Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 2.85
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.5
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.5
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "betonlineag",
                    "title": "BetOnline.ag",
                    "last_update": "2025-01-29T22:32:19Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:19Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 2.9
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.5
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.45
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "everygame",
                    "title": "Everygame",
                    "last_update": "2025-01-29T22:30:58Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:30:58Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 2.8
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.45
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.3
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "matchbook",
                    "title": "Matchbook",
                    "last_update": "2025-01-29T22:32:19Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:19Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 2.96
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.56
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.55
                                }
                            ]
                        },
                        {
                            "key": "h2h_lay",
                            "last_update": "2025-01-29T22:32:19Z",
                            "outcomes": [
                                {
                                    "name": "FSV Mainz 05",
                                    "price": 3
                                },
                                {
                                    "name": "Werder Bremen",
                                    "price": 2.62
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.65
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "id": "ed6eccca4649279d16c320399e56a39b",
            "home_team": "Parma",
            "away_team": "Lecce",
            "bookmakers": [
                {
                    "key": "betclic",
                    "title": "Betclic",
                    "last_update": "2025-01-29T22:31:43Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:31:43Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.47
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.11
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.37
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "onexbet",
                    "title": "1xBet",
                    "last_update": "2025-01-29T22:32:59Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:59Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.5
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.17
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.71
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "tipico_de",
                    "title": "Tipico",
                    "last_update": "2025-01-29T22:33:02Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:33:02Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.4
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.15
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.3
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "marathonbet",
                    "title": "Marathon Bet",
                    "last_update": "2025-01-29T22:33:00Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:33:00Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.38
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.1
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.58
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "pinnacle",
                    "title": "Pinnacle",
                    "last_update": "2025-01-29T22:32:59Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:59Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.52
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.19
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.41
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "sport888",
                    "title": "888sport",
                    "last_update": "2025-01-29T22:32:59Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:32:59Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.3
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.1
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.4
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "williamhill",
                    "title": "William Hill",
                    "last_update": "2025-01-29T22:33:02Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:33:02Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.3
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.1
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.4
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "betsson",
                    "title": "Betsson",
                    "last_update": "2025-01-29T22:33:01Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:33:01Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.35
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.18
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.35
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "nordicbet",
                    "title": "Nordic Bet",
                    "last_update": "2025-01-29T22:33:00Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:33:00Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.4
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.2
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.4
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "unibet_eu",
                    "title": "Unibet",
                    "last_update": "2025-01-29T22:33:02Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:33:02Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.6
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.1
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.6
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "gtbets",
                    "title": "GTbets",
                    "last_update": "2025-01-29T22:33:01Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:33:01Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.46
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.07
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.33
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "everygame",
                    "title": "Everygame",
                    "last_update": "2025-01-29T22:31:32Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:31:32Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.4
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.15
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.3
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "matchbook",
                    "title": "Matchbook",
                    "last_update": "2025-01-29T22:33:00Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:33:00Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.65
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.26
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.5
                                }
                            ]
                        },
                        {
                            "key": "h2h_lay",
                            "last_update": "2025-01-29T22:33:00Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.7
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.28
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.6
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "betfair_ex_eu",
                    "title": "Betfair",
                    "last_update": "2025-01-29T22:33:04Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:33:04Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.65
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.26
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.5
                                }
                            ]
                        },
                        {
                            "key": "h2h_lay",
                            "last_update": "2025-01-29T22:33:04Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.7
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.28
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.55
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "betonlineag",
                    "title": "BetOnline.ag",
                    "last_update": "2025-01-29T22:31:30Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:31:30Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.55
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.18
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.4
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "coolbet",
                    "title": "Coolbet",
                    "last_update": "2025-01-29T22:33:03Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:33:03Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.5
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.16
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.55
                                }
                            ]
                        }
                    ]
                },
                {
                    "key": "betanysports",
                    "title": "BetAnySports",
                    "last_update": "2025-01-29T22:33:00Z",
                    "markets": [
                        {
                            "key": "h2h",
                            "last_update": "2025-01-29T22:33:00Z",
                            "outcomes": [
                                {
                                    "name": "Lecce",
                                    "price": 3.55
                                },
                                {
                                    "name": "Parma",
                                    "price": 2.18
                                },
                                {
                                    "name": "Draw",
                                    "price": 3.4
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
    mapping_table_odds_to_free = Match.create_mapping_table_odds_to_foot_api_paid(leagues)
    pprint(mapping_table_odds_to_free)
    print(len(mapping_table_odds_to_free))

    foot_api_paid_teams = json.load(open('../data/filtered_teams.json', encoding='utf-8'))
    old = [{'ID': 80, 'Name': 'Olympique Lyonnais', 'Country': 'France', 'League': 'Ligue 1'},
           {'ID': 51, 'Name': 'Brighton', 'Country': 'England', 'League': 'Premier League'}]
    # Check team that are not in the mapping table
    print("Teams that are not in the mapping table")
    for team in foot_api_paid_teams:
        if team['Name'] not in mapping_table_odds_to_free:
            print(team)
    # mapping_table_free_to_paid = Match.create_mapping_table_foot_api_free_to_foot_api_paid(leagues)
    # new_match = []
    # for match in match:
    #     actual_match = Match(**match)
    #     match_fixture_id = actual_match.get_fixture(mapping_table_odds_to_free, mapping_table_free_to_paid)
    #     actual_match.set_prediction(match_fixture_id)
    #     new_match.append(actual_match)
    #
    # pprint(new_match)

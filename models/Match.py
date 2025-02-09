
from datetime import datetime
from pprint import pprint
from typing import Optional

import requests
from pydantic import BaseModel

from models.Bookmaker import Bookmaker
from models.Prediction import Prediction, PredictionWinner, PredictionPercent, TeamStat, Last5Matches, Goal, \
    CompetitionTeamStat, Repartition, TeamComparaison
from variable import API_SPORT_KEY


class NoPredictionError(Exception):
    pass


class Match(BaseModel):
    fixture_id: int
    home_team: Optional[str] = None
    away_team: Optional[str] = None
    commence_time: datetime
    bookmakers: list[Bookmaker]
    prediction: Optional[Prediction] = None

    @staticmethod
    def response_data_to_model(data: dict) -> "Match":
        bookmakers = Bookmaker.filter_without_unibet(data['bookmakers'])
        if not bookmakers:
            return None
        return Match(
            fixture_id=data['fixture']['id'],
            commence_time=datetime.fromisoformat(data['fixture']['date']),
            bookmakers=bookmakers
        )

    @staticmethod
    def convert_percent_to_float(percent: str) -> float:
        return float(percent.replace('%', '')) / 100

    @staticmethod
    def get_teams_stat(prediction_teams_data: dict) -> TeamStat:
        return TeamStat(
            last_5_matches_all_competitions=Last5Matches(
                form=prediction_teams_data['last_5']['form'],
                att=prediction_teams_data['last_5']['att'],
                defn=prediction_teams_data['last_5']['def'],
                scored_goal=Goal(total=float(prediction_teams_data['last_5']['goals']['for']['total']),
                                 average=float(prediction_teams_data['last_5']['goals']['for']['average'])),
                conceded_goal=Goal(total=float(prediction_teams_data['last_5']['goals']['against']['total']),
                                   average=float(prediction_teams_data['last_5']['goals']['against']['average']))
            ),
            actual_competition_stat=CompetitionTeamStat(
                form=prediction_teams_data['league']['form'],
                played=Repartition(home=float(prediction_teams_data['league']['fixtures']['played']['home']),
                                   away=float(prediction_teams_data['league']['fixtures']['played']['away']),
                                   total=float(prediction_teams_data['league']['fixtures']['played']['total'])),
                wins=Repartition(home=float(prediction_teams_data['league']['fixtures']['wins']['home']),
                                 away=float(prediction_teams_data['league']['fixtures']['wins']['away']),
                                 total=float(prediction_teams_data['league']['fixtures']['wins']['total'])),
                draws=Repartition(home=float(prediction_teams_data['league']['fixtures']['draws']['home']),
                                  away=float(prediction_teams_data['league']['fixtures']['draws']['away']),
                                  total=float(prediction_teams_data['league']['fixtures']['draws']['total'])),
                loses=Repartition(home=float(prediction_teams_data['league']['fixtures']['loses']['home']),
                                  away=float(prediction_teams_data['league']['fixtures']['loses']['away']),
                                  total=float(prediction_teams_data['league']['fixtures']['loses']['total'])),
                total_scored_goal=Repartition(
                    home=float(prediction_teams_data['league']['goals']['for']['total']['home']),
                    away=float(prediction_teams_data['league']['goals']['for']['total']['away']),
                    total=float(prediction_teams_data['league']['goals']['for']['total']['total'])),
                total_conceded_goal=Repartition(
                    home=float(prediction_teams_data['league']['goals']['against']['total']['home']),
                    away=float(prediction_teams_data['league']['goals']['against']['total']['away']),
                    total=float(prediction_teams_data['league']['goals']['against']['total']['total'])),
                average_scored_goal=Repartition(
                    home=float(prediction_teams_data['league']['goals']['for']['average']['home']),
                    away=float(prediction_teams_data['league']['goals']['for']['average']['away']),
                    total=float(prediction_teams_data['league']['goals']['for']['average']['total'])),
                average_conceded_goal=Repartition(
                    home=float(prediction_teams_data['league']['goals']['against']['average']['home']),
                    away=float(prediction_teams_data['league']['goals']['against']['average']['away']),
                    total=float(prediction_teams_data['league']['goals']['against']['average']['total'])),
                goal_scored_minute_information=prediction_teams_data['league']['goals']['for']['minute'],
                goal_scored_under_over=prediction_teams_data['league']['goals']['for']['under_over'],
                goal_conceded_minute_information=prediction_teams_data['league']['goals']['against']['minute'],
                goal_conceded_under_over=prediction_teams_data['league']['goals']['against']['under_over'],
                clean_sheet_information=Repartition(
                    home=float(prediction_teams_data['league']['clean_sheet']['home']),
                    away=float(prediction_teams_data['league']['clean_sheet']['away']),
                    total=float(prediction_teams_data['league']['clean_sheet']['total'])),
                biggest_information_stat=prediction_teams_data['league']['biggest'],
                failed_to_score_information=Repartition(
                    home=float(prediction_teams_data['league']['failed_to_score']['home']),
                    away=float(prediction_teams_data['league']['failed_to_score']['away']),
                    total=float(prediction_teams_data['league']['failed_to_score']['total']))
            )
        )

    def set_prediction(self) -> None:
        url = f"https://v3.football.api-sports.io/predictions?fixture={self.fixture_id}"
        headers = {
            'x-rapidapi-key': API_SPORT_KEY,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        response = requests.request("GET", url, headers=headers)
        if not response.json()['response']:
            raise NoPredictionError("No prediction found for this match")
        prediction = response.json()['response'][0]
        winner = PredictionWinner(
            name=prediction['predictions']['winner']['name'],
            comment=prediction['predictions']['winner']['comment']
        )
        advice = prediction['predictions']['advice']
        probabilities = PredictionPercent(
            home=Match.convert_percent_to_float(prediction['predictions']['percent']['home']),
            draw=Match.convert_percent_to_float(prediction['predictions']['percent']['draw']),
            away=Match.convert_percent_to_float(prediction['predictions']['percent']['away'])
        )
        home_team = Match.get_teams_stat(prediction['teams']['home'])
        away_team = Match.get_teams_stat(prediction['teams']['away'])
        comparaison = TeamComparaison(
            form=prediction['comparison']['form'],
            att=prediction['comparison']['att'],
            defn=prediction['comparison']['def'],
            h2h=prediction['comparison']['h2h'],
            goals=prediction['comparison']['goals'],
            total=prediction['comparison']['total']
        )
        self.prediction = Prediction(
            winner=winner,
            advice=advice,
            probabilities=probabilities,
            home_team_stat=home_team,
            away_team_stat=away_team,
            comparaison=comparaison
        )
        if not self.home_team:
            self.home_team = prediction['teams']['home']['name']
        if not self.away_team:
            self.away_team = prediction['teams']['away']['name']


if __name__ == "__main__":
    # data = get_history_data('78')
    # pprint(data[0])
    raw_data = {
        "fixture_id": 1208692,
        "home_team": None,
        "away_team": None,
        "commence_time": "2025-02-08T15:15:00Z",
        "bookmakers": [
            {
                "name": "Bwin",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.77
                            },
                            {
                                "value": "Draw",
                                "odd": 3.6
                            },
                            {
                                "value": "Away",
                                "odd": 4.75
                            }
                        ]
                    }
                ]
            },
            {
                "name": "NordicBet",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.78
                            },
                            {
                                "value": "Draw",
                                "odd": 3.75
                            },
                            {
                                "value": "Away",
                                "odd": 4.75
                            }
                        ]
                    }
                ]
            },
            {
                "name": "10Bet",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.73
                            },
                            {
                                "value": "Draw",
                                "odd": 3.65
                            },
                            {
                                "value": "Away",
                                "odd": 4.8
                            }
                        ]
                    }
                ]
            },
            {
                "name": "William Hill",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.75
                            },
                            {
                                "value": "Draw",
                                "odd": 3.7
                            },
                            {
                                "value": "Away",
                                "odd": 4.8
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Bet365",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.73
                            },
                            {
                                "value": "Draw",
                                "odd": 3.6
                            },
                            {
                                "value": "Away",
                                "odd": 5
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Marathonbet",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.73
                            },
                            {
                                "value": "Draw",
                                "odd": 3.8
                            },
                            {
                                "value": "Away",
                                "odd": 4.95
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Unibet",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.72
                            },
                            {
                                "value": "Draw",
                                "odd": 3.6
                            },
                            {
                                "value": "Away",
                                "odd": 4.8
                            }
                        ]
                    },
                    {
                        "name": "Home/Away",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.29
                            },
                            {
                                "value": "Away",
                                "odd": 3.45
                            }
                        ]
                    },
                    {
                        "name": "Second Half Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 2.12
                            },
                            {
                                "value": "Draw",
                                "odd": 2.55
                            },
                            {
                                "value": "Away",
                                "odd": 4.6
                            }
                        ]
                    },
                    {
                        "name": "Goals Over/Under",
                        "values": [
                            {
                                "value": "Over 1.5",
                                "odd": 1.3
                            },
                            {
                                "value": "Under 1.5",
                                "odd": 3.35
                            },
                            {
                                "value": "Over 1.75",
                                "odd": 1.42
                            },
                            {
                                "value": "Under 1.75",
                                "odd": 2.88
                            },
                            {
                                "value": "Over 2.0",
                                "odd": 1.54
                            },
                            {
                                "value": "Under 2.0",
                                "odd": 2.45
                            },
                            {
                                "value": "Over 2.25",
                                "odd": 1.79
                            },
                            {
                                "value": "Under 2.25",
                                "odd": 2
                            },
                            {
                                "value": "Over 2.5",
                                "odd": 2.05
                            },
                            {
                                "value": "Under 2.5",
                                "odd": 1.76
                            },
                            {
                                "value": "Over 2.75",
                                "odd": 2.35
                            },
                            {
                                "value": "Under 2.75",
                                "odd": 1.57
                            },
                            {
                                "value": "Over 3.5",
                                "odd": 3.85
                            },
                            {
                                "value": "Under 3.5",
                                "odd": 1.24
                            },
                            {
                                "value": "Over 0.5",
                                "odd": 1.03
                            },
                            {
                                "value": "Under 0.5",
                                "odd": 10.5
                            },
                            {
                                "value": "Over 3.0",
                                "odd": 2.95
                            },
                            {
                                "value": "Under 3.0",
                                "odd": 1.38
                            },
                            {
                                "value": "Over 4.5",
                                "odd": 8
                            },
                            {
                                "value": "Under 4.5",
                                "odd": 1.06
                            },
                            {
                                "value": "Over 3.25",
                                "odd": 3.35
                            },
                            {
                                "value": "Under 3.25",
                                "odd": 1.3
                            }
                        ]
                    },
                    {
                        "name": "Goals Over/Under First Half",
                        "values": [
                            {
                                "value": "Over 1.5",
                                "odd": 3
                            },
                            {
                                "value": "Under 1.5",
                                "odd": 1.38
                            },
                            {
                                "value": "Over 1.75",
                                "odd": 3.9
                            },
                            {
                                "value": "Under 1.75",
                                "odd": 1.24
                            },
                            {
                                "value": "Over 2.0",
                                "odd": 6.5
                            },
                            {
                                "value": "Under 2.0",
                                "odd": 1.1
                            },
                            {
                                "value": "Over 2.5",
                                "odd": 6.75
                            },
                            {
                                "value": "Under 2.5",
                                "odd": 1.06
                            },
                            {
                                "value": "Over 0.5",
                                "odd": 1.41
                            },
                            {
                                "value": "Under 0.5",
                                "odd": 2.65
                            },
                            {
                                "value": "Over 0.75",
                                "odd": 1.58
                            },
                            {
                                "value": "Under 0.75",
                                "odd": 2.32
                            },
                            {
                                "value": "Over 1.0",
                                "odd": 1.96
                            },
                            {
                                "value": "Under 1.0",
                                "odd": 1.8
                            },
                            {
                                "value": "Over 1.25",
                                "odd": 2.48
                            },
                            {
                                "value": "Under 1.25",
                                "odd": 1.5
                            }
                        ]
                    },
                    {
                        "name": "Goals Over/Under - Second Half",
                        "values": [
                            {
                                "value": "Over 1.5",
                                "odd": 2.18
                            },
                            {
                                "value": "Under 1.5",
                                "odd": 1.58
                            },
                            {
                                "value": "Over 2.5",
                                "odd": 4.6
                            },
                            {
                                "value": "Under 2.5",
                                "odd": 1.15
                            },
                            {
                                "value": "Over 3.5",
                                "odd": 11.5
                            },
                            {
                                "value": "Under 3.5",
                                "odd": 1.02
                            },
                            {
                                "value": "Over 0.5",
                                "odd": 1.24
                            },
                            {
                                "value": "Under 0.5",
                                "odd": 3.55
                            }
                        ]
                    },
                    {
                        "name": "HT/FT Double",
                        "values": [
                            {
                                "value": "Home/Draw",
                                "odd": 14
                            },
                            {
                                "value": "Home/Away",
                                "odd": 51
                            },
                            {
                                "value": "Draw/Away",
                                "odd": 9.5
                            },
                            {
                                "value": "Draw/Draw",
                                "odd": 5.1
                            },
                            {
                                "value": "Home/Home",
                                "odd": 2.7
                            },
                            {
                                "value": "Draw/Home",
                                "odd": 4.3
                            },
                            {
                                "value": "Away/Home",
                                "odd": 23
                            },
                            {
                                "value": "Away/Draw",
                                "odd": 15
                            },
                            {
                                "value": "Away/Away",
                                "odd": 7.5
                            }
                        ]
                    },
                    {
                        "name": "Both Teams Score",
                        "values": [
                            {
                                "value": "Yes",
                                "odd": 1.94
                            },
                            {
                                "value": "No",
                                "odd": 1.8
                            }
                        ]
                    },
                    {
                        "name": "Handicap Result",
                        "values": [
                            {
                                "value": "Home -1",
                                "odd": 3.15
                            },
                            {
                                "value": "Away -1",
                                "odd": 2.06
                            },
                            {
                                "value": "Draw -1",
                                "odd": 3.35
                            },
                            {
                                "value": "Home -2",
                                "odd": 7
                            },
                            {
                                "value": "Draw -2",
                                "odd": 5.1
                            },
                            {
                                "value": "Away -2",
                                "odd": 1.33
                            }
                        ]
                    },
                    {
                        "name": "Exact Score",
                        "values": [
                            {
                                "value": "1:0",
                                "odd": 6.1
                            },
                            {
                                "value": "2:0",
                                "odd": 7
                            },
                            {
                                "value": "2:1",
                                "odd": 7.5
                            },
                            {
                                "value": "3:0",
                                "odd": 12.5
                            },
                            {
                                "value": "3:1",
                                "odd": 14
                            },
                            {
                                "value": "3:2",
                                "odd": 26
                            },
                            {
                                "value": "4:0",
                                "odd": 30
                            },
                            {
                                "value": "4:1",
                                "odd": 36
                            },
                            {
                                "value": "0:0",
                                "odd": 9.5
                            },
                            {
                                "value": "1:1",
                                "odd": 6.4
                            },
                            {
                                "value": "2:2",
                                "odd": 16
                            },
                            {
                                "value": "0:1",
                                "odd": 11.5
                            },
                            {
                                "value": "0:2",
                                "odd": 23
                            },
                            {
                                "value": "0:3",
                                "odd": 67
                            },
                            {
                                "value": "1:2",
                                "odd": 14
                            },
                            {
                                "value": "1:3",
                                "odd": 46
                            },
                            {
                                "value": "2:3",
                                "odd": 51
                            },
                            {
                                "value": "3:3",
                                "odd": 81
                            },
                            {
                                "value": "1:4",
                                "odd": 181
                            },
                            {
                                "value": "2:4",
                                "odd": 226
                            },
                            {
                                "value": "4:2",
                                "odd": 56
                            },
                            {
                                "value": "5:0",
                                "odd": 81
                            },
                            {
                                "value": "5:1",
                                "odd": 111
                            },
                            {
                                "value": "5:2",
                                "odd": 201
                            },
                            {
                                "value": "6:0",
                                "odd": 226
                            },
                            {
                                "value": "4:3",
                                "odd": 226
                            }
                        ]
                    },
                    {
                        "name": "Correct Score - First Half",
                        "values": [
                            {
                                "value": "1:0",
                                "odd": 3.5
                            },
                            {
                                "value": "2:0",
                                "odd": 9
                            },
                            {
                                "value": "2:1",
                                "odd": 21
                            },
                            {
                                "value": "3:0",
                                "odd": 31
                            },
                            {
                                "value": "3:1",
                                "odd": 81
                            },
                            {
                                "value": "4:0",
                                "odd": 201
                            },
                            {
                                "value": "0:0",
                                "odd": 2.7
                            },
                            {
                                "value": "1:1",
                                "odd": 8
                            },
                            {
                                "value": "2:2",
                                "odd": 91
                            },
                            {
                                "value": "0:1",
                                "odd": 6.4
                            },
                            {
                                "value": "0:2",
                                "odd": 26
                            },
                            {
                                "value": "0:3",
                                "odd": 151
                            },
                            {
                                "value": "1:2",
                                "odd": 36
                            },
                            {
                                "value": "1:3",
                                "odd": 251
                            }
                        ]
                    },
                    {
                        "name": "Double Chance",
                        "values": [
                            {
                                "value": "Home/Draw",
                                "odd": 1.18
                            },
                            {
                                "value": "Home/Away",
                                "odd": 1.28
                            },
                            {
                                "value": "Draw/Away",
                                "odd": 2.04
                            }
                        ]
                    },
                    {
                        "name": "First Half Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 2.35
                            },
                            {
                                "value": "Draw",
                                "odd": 2.17
                            },
                            {
                                "value": "Away",
                                "odd": 5
                            }
                        ]
                    },
                    {
                        "name": "Total - Home",
                        "values": [
                            {
                                "value": "Over 1.5",
                                "odd": 1.9
                            },
                            {
                                "value": "Under 1.5",
                                "odd": 1.8
                            },
                            {
                                "value": "Over 2.5",
                                "odd": 3.9
                            },
                            {
                                "value": "Under 2.5",
                                "odd": 1.21
                            },
                            {
                                "value": "Over 3.5",
                                "odd": 8.5
                            },
                            {
                                "value": "Under 3.5",
                                "odd": 1.04
                            },
                            {
                                "value": "Over 0.5",
                                "odd": 1.17
                            },
                            {
                                "value": "Under 0.5",
                                "odd": 4.35
                            }
                        ]
                    },
                    {
                        "name": "Total - Away",
                        "values": [
                            {
                                "value": "Over 1.5",
                                "odd": 3.8
                            },
                            {
                                "value": "Under 1.5",
                                "odd": 1.22
                            },
                            {
                                "value": "Over 2.5",
                                "odd": 9.5
                            },
                            {
                                "value": "Under 2.5",
                                "odd": 1.03
                            },
                            {
                                "value": "Over 0.5",
                                "odd": 1.58
                            },
                            {
                                "value": "Under 0.5",
                                "odd": 2.18
                            }
                        ]
                    },
                    {
                        "name": "Double Chance - First Half",
                        "values": [
                            {
                                "value": "Home/Draw",
                                "odd": 1.13
                            },
                            {
                                "value": "Home/Away",
                                "odd": 1.6
                            },
                            {
                                "value": "Draw/Away",
                                "odd": 1.5
                            }
                        ]
                    },
                    {
                        "name": "Corners 1x2",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.49
                            },
                            {
                                "value": "Draw",
                                "odd": 7
                            },
                            {
                                "value": "Away",
                                "odd": 2.9
                            }
                        ]
                    },
                    {
                        "name": "Corners Over Under",
                        "values": [
                            {
                                "value": "Over 8.5",
                                "odd": 1.58
                            },
                            {
                                "value": "Under 8.5",
                                "odd": 2.18
                            },
                            {
                                "value": "Over 9.5",
                                "odd": 1.95
                            },
                            {
                                "value": "Under 9.5",
                                "odd": 1.75
                            },
                            {
                                "value": "Over 10.5",
                                "odd": 2.48
                            },
                            {
                                "value": "Under 10.5",
                                "odd": 1.46
                            },
                            {
                                "value": "Over 4.5",
                                "odd": 1.01
                            },
                            {
                                "value": "Under 4.5",
                                "odd": 9.5
                            },
                            {
                                "value": "Over 7.5",
                                "odd": 1.34
                            },
                            {
                                "value": "Under 7.5",
                                "odd": 2.9
                            },
                            {
                                "value": "Over 5.5",
                                "odd": 1.08
                            },
                            {
                                "value": "Under 5.5",
                                "odd": 6.1
                            },
                            {
                                "value": "Over 11.5",
                                "odd": 3.2
                            },
                            {
                                "value": "Under 11.5",
                                "odd": 1.29
                            },
                            {
                                "value": "Over 12.5",
                                "odd": 4.3
                            },
                            {
                                "value": "Under 12.5",
                                "odd": 1.17
                            },
                            {
                                "value": "Over 6.5",
                                "odd": 1.19
                            },
                            {
                                "value": "Under 6.5",
                                "odd": 4.1
                            },
                            {
                                "value": "Over 13.5",
                                "odd": 5.6
                            },
                            {
                                "value": "Under 13.5",
                                "odd": 1.1
                            },
                            {
                                "value": "Over 14.5",
                                "odd": 7
                            },
                            {
                                "value": "Under 14.5",
                                "odd": 1.05
                            }
                        ]
                    },
                    {
                        "name": "Home Team Total Goals(1st Half)",
                        "values": [
                            {
                                "value": "Over 1.5",
                                "odd": 4.9
                            },
                            {
                                "value": "Under 1.5",
                                "odd": 1.13
                            },
                            {
                                "value": "Over 0.5",
                                "odd": 1.79
                            },
                            {
                                "value": "Under 0.5",
                                "odd": 1.91
                            }
                        ]
                    },
                    {
                        "name": "Away Team Total Goals(1st Half)",
                        "values": [
                            {
                                "value": "Over 1.5",
                                "odd": 10
                            },
                            {
                                "value": "Under 1.5",
                                "odd": 1.03
                            },
                            {
                                "value": "Over 0.5",
                                "odd": 2.75
                            },
                            {
                                "value": "Under 0.5",
                                "odd": 1.38
                            }
                        ]
                    },
                    {
                        "name": "Draw No Bet (1st Half)",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.36
                            },
                            {
                                "value": "Away",
                                "odd": 2.9
                            }
                        ]
                    },
                    {
                        "name": "Draw No Bet (2nd Half)",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.34
                            },
                            {
                                "value": "Away",
                                "odd": 2.8
                            }
                        ]
                    },
                    {
                        "name": "Home Corners Over/Under",
                        "values": [
                            {
                                "value": "Over 3.5",
                                "odd": 1.26
                            },
                            {
                                "value": "Under 3.5",
                                "odd": 3.4
                            },
                            {
                                "value": "Over 8.5",
                                "odd": 4.8
                            },
                            {
                                "value": "Under 8.5",
                                "odd": 1.14
                            },
                            {
                                "value": "Over 4.5",
                                "odd": 1.53
                            },
                            {
                                "value": "Under 4.5",
                                "odd": 2.3
                            },
                            {
                                "value": "Over 7.5",
                                "odd": 3.45
                            },
                            {
                                "value": "Under 7.5",
                                "odd": 1.25
                            },
                            {
                                "value": "Over 5.5",
                                "odd": 1.96
                            },
                            {
                                "value": "Under 5.5",
                                "odd": 1.73
                            },
                            {
                                "value": "Over 6.5",
                                "odd": 2.55
                            },
                            {
                                "value": "Under 6.5",
                                "odd": 1.44
                            }
                        ]
                    },
                    {
                        "name": "Away Corners Over/Under",
                        "values": [
                            {
                                "value": "Over 2.5",
                                "odd": 1.38
                            },
                            {
                                "value": "Under 2.5",
                                "odd": 2.7
                            },
                            {
                                "value": "Over 3.5",
                                "odd": 1.84
                            },
                            {
                                "value": "Under 3.5",
                                "odd": 1.84
                            },
                            {
                                "value": "Over 4.5",
                                "odd": 2.55
                            },
                            {
                                "value": "Under 4.5",
                                "odd": 1.44
                            },
                            {
                                "value": "Over 5.5",
                                "odd": 3.8
                            },
                            {
                                "value": "Under 5.5",
                                "odd": 1.21
                            },
                            {
                                "value": "Over 6.5",
                                "odd": 5.4
                            },
                            {
                                "value": "Under 6.5",
                                "odd": 1.1
                            }
                        ]
                    },
                    {
                        "name": "Total Corners (1st Half)",
                        "values": [
                            {
                                "value": "Over 3.5",
                                "odd": 1.45
                            },
                            {
                                "value": "Under 3.5",
                                "odd": 2.43
                            },
                            {
                                "value": "Over 4.5",
                                "odd": 1.97
                            },
                            {
                                "value": "Under 4.5",
                                "odd": 1.7
                            },
                            {
                                "value": "Over 5.5",
                                "odd": 2.8
                            },
                            {
                                "value": "Under 5.5",
                                "odd": 1.35
                            }
                        ]
                    },
                    {
                        "name": "Cards Over/Under",
                        "values": [
                            {
                                "value": "Over 2.5",
                                "odd": 1.11
                            },
                            {
                                "value": "Under 2.5",
                                "odd": 5.1
                            },
                            {
                                "value": "Over 3.5",
                                "odd": 1.33
                            },
                            {
                                "value": "Under 3.5",
                                "odd": 2.95
                            },
                            {
                                "value": "Over 4.5",
                                "odd": 1.71
                            },
                            {
                                "value": "Under 4.5",
                                "odd": 2
                            },
                            {
                                "value": "Over 7.5",
                                "odd": 4.6
                            },
                            {
                                "value": "Under 7.5",
                                "odd": 1.15
                            },
                            {
                                "value": "Over 5.5",
                                "odd": 2.3
                            },
                            {
                                "value": "Under 5.5",
                                "odd": 1.54
                            },
                            {
                                "value": "Over 6.5",
                                "odd": 3.2
                            },
                            {
                                "value": "Under 6.5",
                                "odd": 1.28
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Betfair",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.75
                            },
                            {
                                "value": "Draw",
                                "odd": 3.75
                            },
                            {
                                "value": "Away",
                                "odd": 5
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Betsson",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.78
                            },
                            {
                                "value": "Draw",
                                "odd": 3.75
                            },
                            {
                                "value": "Away",
                                "odd": 4.75
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Fonbet",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.75
                            },
                            {
                                "value": "Draw",
                                "odd": 3.8
                            },
                            {
                                "value": "Away",
                                "odd": 5
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Pinnacle",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.77
                            },
                            {
                                "value": "Draw",
                                "odd": 3.8
                            },
                            {
                                "value": "Away",
                                "odd": 4.97
                            }
                        ]
                    }
                ]
            },
            {
                "name": "SBO",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.77
                            },
                            {
                                "value": "Draw",
                                "odd": 3.35
                            },
                            {
                                "value": "Away",
                                "odd": 4.3
                            }
                        ]
                    }
                ]
            },
            {
                "name": "1xBet",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.78
                            },
                            {
                                "value": "Draw",
                                "odd": 3.91
                            },
                            {
                                "value": "Away",
                                "odd": 5.04
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Betano",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.78
                            },
                            {
                                "value": "Draw",
                                "odd": 3.65
                            },
                            {
                                "value": "Away",
                                "odd": 4.6
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Betway",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.75
                            },
                            {
                                "value": "Draw",
                                "odd": 3.75
                            },
                            {
                                "value": "Away",
                                "odd": 4.5
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Tipico",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.72
                            },
                            {
                                "value": "Draw",
                                "odd": 3.7
                            },
                            {
                                "value": "Away",
                                "odd": 4.8
                            }
                        ]
                    }
                ]
            },
            {
                "name": "888Sport",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.75
                            },
                            {
                                "value": "Draw",
                                "odd": 3.7
                            },
                            {
                                "value": "Away",
                                "odd": 4.8
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Dafabet",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {
                                "value": "Home",
                                "odd": 1.79
                            },
                            {
                                "value": "Draw",
                                "odd": 3.55
                            },
                            {
                                "value": "Away",
                                "odd": 4.75
                            }
                        ]
                    }
                ]
            }
        ],
        "prediction": None
    }
    match = Match(**raw_data)
    # pprint(raw_data)
    match.set_prediction()
    pprint(match.model_dump())

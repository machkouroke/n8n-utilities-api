import enum
import json
from datetime import datetime
from pprint import pprint
from typing import Optional

import requests

from pydantic import BaseModel

from models.Bookmaker import Bookmaker
from models.League import League
from variable import API_SPORT_KEY


class Match(BaseModel):
    fixture_id: int
    home_team: Optional[str] = None
    away_team: Optional[str] = None
    commence_time: datetime
    bookmakers: list[Bookmaker]
    prediction: Optional[dict] = None

    @staticmethod
    def response_data_to_model(data: dict) -> "Match":
        bookmakers= Bookmaker.filter_without_unibet(data['bookmakers'])
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

    def set_prediction(self, fixture_id: int) -> None:
        url = f"https://v3.football.api-sports.io/predictions?fixture={fixture_id}"
        headers = {
            'x-rapidapi-value': API_SPORT_KEY,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        response = requests.request("GET", url, headers=headers)
        if not response.json()['response']:
            return
        self.prediction = response.json()['response'][0]


if __name__ == "__main__":
    # data = get_history_data('78')
    # pprint(data[0])
    leagues = (
        League(**{"value": "La liga", "odds_api_id": "soccer_spain_la_liga",
                  "foot_api_free_id": 2014,

                  "foot_api_paid_name": "Spain"
                  }),
        League(**{"value": "Premier League",
                  "foot_api_paid_name": "England",
                  "odds_api_id": "soccer_england_league1", "foot_api_free_id": 2021}),
        League(**{"value": "Bundesliga", "odds_api_id": "soccer_germany_bundesliga",
                  "foot_api_paid_name": "Germany",
                  "foot_api_free_id": 2002}),
        League(**{"value": "Serie A", "odds_api_id": "soccer_italy_serie_a", "foot_api_free_id": 2019,
                  "foot_api_paid_name": "Italy"}),
        League(**{"value": "Ligue 1", "odds_api_id": "soccer_france_ligue_one", "foot_api_free_id": 2015,
                  "foot_api_paid_name": "France"}),
    )

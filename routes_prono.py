from datetime import datetime
from pprint import pprint

import requests
from fastapi import APIRouter, Query

from models.League import League
from models.Match import Match, NoPredictionError
from variable import API_SPORT_KEY

router = APIRouter()


# leagues = (
#     League(**{"value": "La liga", "odds_api_id":
#         "soccer_spain_la_liga",
#               "foot_api_free_id": 2014,
#               "foot_api_paid_name": "Spain",
#               "foot_api_paid_id": 2014
#               }),
#     League(**{"value": "Premier League",
#               "foot_api_paid_name": "England",
#               "odds_api_id": "soccer_england_league1", "foot_api_free_id": 2021}),
#     League(**{"value": "Bundesliga", "odds_api_id": "soccer_germany_bundesliga",
#               "foot_api_paid_name": "Germany",
#               "foot_api_free_id": 2002}),
#     League(**{"value": "Serie A", "odds_api_id": "soccer_italy_serie_a", "foot_api_free_id": 2019,
#               "foot_api_paid_name": "Italy"}),
#     League(**{"value": "Ligue 1", "odds_api_id": "soccer_france_ligue_one", "foot_api_free_id": 2015,
#               "foot_api_paid_name": "France"}),
# )

@router.post("/odds")
def get_odd(leagues: list[League], date: str = Query(..., regex=r"^\d{4}-\d{2}-\d{2}$")):
    """
    Get the odds of a match
    :param date:
    :param leagues:
    :return: the odds of the match
    """
    url = "https://v3.football.api-sports.io/odds"
    matchs = []
    headers = {
        'x-rapidapi-key': API_SPORT_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    for league in leagues:
        querystring = {"league": league.api_sport, "season": league.season, "date": date}
        response = requests.request("GET", url, headers=headers, params=querystring)
        matchs_data = response.json()["response"]
        for match in matchs_data:
            new_match = Match.response_data_to_model(match)
            if new_match.bookmakers:
                matchs.append(new_match)
    return {
        "detail": {
            "matchs": matchs,
            "number_of_matchs": len(matchs)
        }
    }


@router.post("/predict")
async def get_predictions(match: Match):
    """
    Get the mapping table of the teams between the odds API and the football API
    :param match:
    :return: the mapping table in a dict
    """
    try:
        match.set_prediction()
        return match
    except NoPredictionError:
        return None

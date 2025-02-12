import requests
from fastapi import APIRouter, Query

from models.League import League
from models.Match import Match, NoPredictionError
from variable import API_SPORT_KEY

router = APIRouter()


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

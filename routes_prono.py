from fastapi import APIRouter

from models.League import League
from models.Match import Match

router = APIRouter()

leagues = [
    League(**{"name": "La liga", "odds_api_id":
        "soccer_spain_la_liga",
              "foot_api_free_id": 2014,
              "foot_api_paid_name": "Spain",
              "foot_api_paid_id": 2014
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


@router.get("/leagues")
async def get_leagues():
    """
    Get the list of leagues
    :return: the list of leagues
    """
    return {
        "detail": {
            "leagues": leagues
        }
    }


@router.post("/predict")
async def get_predictions(matchs: list[Match]):
    """
    Get the mapping table of the teams between the odds API and the football API
    :param matchs:
    :return: the mapping table in a dict
    """
    mapping_table_odds_to_paid = Match.create_mapping_table_odds_to_foot_api_paid(leagues)
    new_match = []
    for match in matchs:
        match_fixture_id = match.get_fixture(mapping_table_odds_to_paid)
        if match_fixture_id != -1:
            match.set_prediction(match_fixture_id)
            new_match.append(match)
    return {
        "detail": {
            "match": new_match,
            'number_of_matches': len(new_match),
            'old_number_of_matches': len(matchs)
        }
    }

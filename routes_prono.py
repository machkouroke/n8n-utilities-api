from fastapi import APIRouter

from models.League import League
from utilities import create_mapping_table_odds_to_footapifree

router = APIRouter()

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


@router.post("/mapping-table")
async def get_mapping_table(leagues: list[League]):
    """
    Get the mapping table of the teams between the odds API and the football API
    :param leagues: the list of leagues to compare
    :return: the mapping table in a dict
    """
    mapping_table = create_mapping_table_odds_to_footapifree(leagues)
    return {
        "detail": {
            "mapping_table": mapping_table,
            "nb_teams_mapped": len(mapping_table)
        }
    }


@router.get('/historical-data')
async def get_historical_data(home_team_id: int, away_team_id: int):
    """
    Get the historical data of the matches
    :return: the historical data
    """
    return {
        "detail": {

        }
    }

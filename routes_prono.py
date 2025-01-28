from fastapi import APIRouter

from models.League import League
from utilities import create_mapping_table

router = APIRouter()

leagues = [
    League(**{"league": "La liga", "api_key": "soccer_spain_la_liga", "api_id": 2014}),
    League(**{"league": "Premier League", "api_key": "soccer_england_league1", "api_id": 2021}),
    League(**{"league": "Bundesliga", "api_key": "soccer_germany_bundesliga", "api_id": 2002}),
    League(**{"league": "Serie A", "api_key": "soccer_italy_serie_a", "api_id": 2019})
]


@router.get("leagues")
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
    mapping_table = create_mapping_table(leagues)
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

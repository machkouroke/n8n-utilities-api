from fastapi import APIRouter

from models.League import League
from utilities import create_mapping_table

router = APIRouter()


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

@router.get('/historical-data/{teams_id}')
async def get_historical_data():
    """
    Get the historical data of the matches
    :return: the historical data
    """
    return {
        "detail": {
            "historical_data": "data"
        }
    }

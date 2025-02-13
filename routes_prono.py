from datetime import datetime

import requests
from fastapi import APIRouter, Query, HTTPException, Depends
from jinja2 import Template, Environment, FileSystemLoader
from pydantic import BaseModel
from pymongo.synchronous.database import Database

from dependencies.db import get_db
from models.Coupons import CouponsData
from models.League import League
from models.Match import Match, NoPredictionError
from variable import API_SPORT_KEY

router = APIRouter()

environment = Environment(loader=FileSystemLoader("template/"))


# Endpoint pour générer une image à partir d'un template HTML et de données
@router.post("/coupon")
def saveCoupon(data: CouponsData, db: Database = Depends(get_db)):
    data.database = db
    # Date of now in format dd/mm/yyyy
    data.date_of_match = datetime.now().strftime("%d-%m-%Y")
    data.save_or_update()
    return data



@router.get("/coupon/{date_of_match}")
def getCoupon(date_of_match: str, db: Database = Depends(get_db)):
    try:
        coupon = CouponsData.find_one(db, date_of_match)
        extremum_date = CouponsData.get_extremum_date(db)
        print(extremum_date)
        return {
            "detail": {
                "coupon": coupon,
                "max_date": extremum_date["date_plus_recente"],
                "min_date": extremum_date["date_plus_ancienne"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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

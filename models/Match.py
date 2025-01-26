from datetime import datetime

from pydantic import BaseModel


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


class Match(BaseModel):
    id: str
    home_team: str
    away_team: str
    bookmakers: list[Bookmaker]

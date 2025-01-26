from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.FootballAPI import Historical


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
    historical: Optional[Historical]

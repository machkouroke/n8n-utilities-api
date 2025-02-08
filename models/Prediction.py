import enum
from typing import Optional

from pydantic import BaseModel, TypeAdapter
from typing_extensions import TypeAliasType


class PredictionPercent(BaseModel):
    home: float
    draw: float
    away: float


class PredictionWinner(BaseModel):
    name: str
    comment: Optional[str]


class Goal(BaseModel):
    total: float
    average: float


class Last5Matches(BaseModel):
    form: str
    conceded_goal: Goal
    scored_goal: Goal


class Repartition(BaseModel):
    home: float
    away: float
    total: float


class CompetitionTeamStat(BaseModel):
    form: str
    wins: Repartition
    draws: Repartition
    loses: Repartition
    total_scored_goal: Repartition
    total_conceded_goal: Repartition


class TeamStat(BaseModel):
    last_5_matches_all_competitions: Last5Matches
    actual_competition_stat: CompetitionTeamStat


class TeamComparaison(BaseModel):
    form: dict[str, str]
    att: dict[str, str]
    defn: dict[str, str]
    total: dict[str, str]


class Prediction(BaseModel):
    winner: PredictionWinner
    advice: str
    probabilities: PredictionPercent
    home_team_stat: TeamStat
    away_team_stat: TeamStat

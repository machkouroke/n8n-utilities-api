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
    att: str
    defn: str
    conceded_goal: Goal
    scored_goal: Goal


class Repartition(BaseModel):
    home: float
    away: float
    total: float


class CompetitionTeamStat(BaseModel):
    form: str
    played: Repartition
    wins: Repartition
    draws: Repartition
    loses: Repartition
    total_scored_goal: Repartition
    total_conceded_goal: Repartition
    average_scored_goal: Repartition
    average_conceded_goal: Repartition
    goal_scored_minute_information: dict
    goal_scored_under_over: dict
    goal_conceded_minute_information: dict
    goal_conceded_under_over: dict
    clean_sheet_information: Repartition
    biggest_information_stat: dict
    failed_to_score_information: Repartition


class TeamStat(BaseModel):
    last_5_matches_all_competitions: Last5Matches
    actual_competition_stat: CompetitionTeamStat


class TeamComparaison(BaseModel):
    form: dict[str, str]
    att: dict[str, str]
    defn: dict[str, str]
    poisson_distribution: dict[str, str]
    h2h: dict[str, str]
    goals: dict[str, str]
    total: dict[str, str]


class Prediction(BaseModel):
    winner: PredictionWinner
    goals: dict[str, float]
    advice: str
    probabilities: PredictionPercent
    home_team_stat: TeamStat
    away_team_stat: TeamStat
    comparaison: TeamComparaison

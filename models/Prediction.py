from pydantic import BaseModel


class Form(enum.Enum):
    W = "W"
    D = "D"
    L = "L"


class PredictionPercent(BaseModel):
    home: float
    draw: float
    away: float


class PredictionWinner(BaseModel):
    name: str
    comment: str


class Goal(BaseModel):
    total: float
    average: float


class Last5Matches(BaseModel):
    att: float
    defn: float
    conceded_goal: Goal
    scored_goal: Goal


class Repartition(BaseModel):
    home: float
    away: float
    total: float


class CompetitionTeamStat(BaseModel):
    form: list[Form]
    played: Repartition
    wins: Repartition
    draws: Repartition
    loses: Repartition
    total_scored_goal: Repartition
    total_conceded_goal: Repartition
    average_scored_goal: Repartition
    average_conceded_goal: Repartition


class TeamStat(BaseModel):
    last_5_matches_all_competitions: Last5Matches
    actual_competition_stat: CompetitionTeamStat

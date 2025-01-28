from datetime import datetime
from typing import List, Optional
import requests

from pydantic import BaseModel


class Repartition(BaseModel):
    home: int
    away: int


# Sous-classes pour les objets imbriqués
class Area(BaseModel):
    code: str
    flag: str
    id: int
    name: str


class Team(BaseModel):
    crest: str
    id: int
    name: str
    shortName: str
    tla: str


class Competition(BaseModel):
    id: int
    name: str
    type: str
    nationality: Optional[str] = None


class Referee(BaseModel):
    id: int
    name: str
    code: Optional[str] = None
    type: str
    emblem: Optional[str] = None


class Score(BaseModel):
    duration: str
    fullTime: Repartition
    halfTime: Repartition
    winner: str


class Season(BaseModel):
    currentMatchday: int
    endDate: str
    id: int
    startDate: str
    winner: Optional[str] = None


class Odds(BaseModel):
    msg: str


class LastMatch(BaseModel):
    win: Repartition
    loss: Repartition
    draw: Repartition
    goal_conceded: Repartition
    goal_scored: Repartition


# Classe principale pour le match
class MatchAPI(BaseModel):
    area: Area
    awayTeam: Team
    competition: Competition
    group: Optional[str] = None
    homeTeam: Team
    id: int
    lastUpdated: datetime
    matchday: int
    odds: Odds
    referees: List[Referee]
    score: Score
    season: Season
    stage: str
    status: str
    utcDate: datetime

    @staticmethod
    def summary(teams_id: int, n=5):
        """
        Give the summaries of the last n matches
        :param teams_id:  Team id
        :param n:  Number of matches to summarize
        :return:  List of summaries
        """

        url = f"https://api.football-data.org/v4/teams/{teams_id}/matches?status=FINISHED"

        headers = {
            'X-Auth-Token': '842e19d260114497a718642c69858dfa'
        }

        response = requests.request("GET", url, headers=headers)
        reverse_match = sorted(response.json()['matches'], key=lambda x: datetime.strptime(x['utcDate'], '%Y-%m-%dT%H'
                                                                                                         ':%M:%S%z'),
                               reverse=True)
        last_n_matches_home = [
                                  MatchAPI(**match) for match in
                                  reverse_match if match['homeTeam']['id'] == int(teams_id)][:n]
        last_n_matches_away = [
                                  MatchAPI(**match) for match in
                                  reverse_match if match['awayTeam']['id'] == int(teams_id)][:n]

        return LastMatch(
            win=Repartition(home=len([match for match in last_n_matches_home if match.score.winner == 'HOME_TEAM']),
                            away=len([match for match in last_n_matches_away if match.score.winner == 'AWAY_TEAM'])),
            loss=Repartition(home=len([match for match in last_n_matches_home if match.score.winner == 'AWAY_TEAM']),
                             away=len([match for match in last_n_matches_away if match.score.winner == 'HOME_TEAM'])),
            draw=Repartition(home=len([match for match in last_n_matches_home if match.score.winner == 'DRAW']),
                             away=len([match for match in last_n_matches_away if match.score.winner == 'DRAW'])),
            goal_conceded=Repartition(home=sum([match.score.fullTime.away for match in last_n_matches_home]),
                                      away=sum([match.score.fullTime.home for match in last_n_matches_away])),
            goal_scored=Repartition(home=sum([match.score.fullTime.home for match in last_n_matches_home]),
                                    away=sum([match.score.fullTime.away for match in last_n_matches_away]))
        )


class Historical(BaseModel):
    last_five_match_home_team: LastMatch
    last_five_match_away_team: LastMatch
    last_five_head_to_head_match_home_win: int
    last_five_head_to_head_match_away_win: int
    injury_indicator: float  # I need to find how to compute
    weather: str

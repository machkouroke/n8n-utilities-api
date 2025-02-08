from pydantic import BaseModel


class League(BaseModel):
    season: int
    league: str
    api_sport: int

    def __eq__(self, other):
        return self.season == other.season and self.league == other.league and self.api_sport == other.api_sport

    def __hash__(self):
        return hash((self.season, self.league, self.api_sport))

    def clean_data(self, leagues_match: list[dict]):
        pass

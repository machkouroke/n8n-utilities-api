from pydantic import BaseModel


class League(BaseModel):
    league: str
    api_key: str
    api_id: int

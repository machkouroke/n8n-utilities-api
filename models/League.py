from pydantic import BaseModel


class League(BaseModel):
    name: str
    odds_api_id: str
    foot_api_free_id: int
    foot_api_paid_name: str


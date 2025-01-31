from pydantic import BaseModel


class League(BaseModel):
    name: str
    odds_api_id: str
    foot_api_free_id: int
    foot_api_paid_name: str

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

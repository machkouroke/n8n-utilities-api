from typing import Optional, Any

from fastapi import HTTPException
from pydantic import BaseModel, Field
from pymongo.synchronous.database import Database
from starlette import status

from dependencies.objectid import PydanticObjectId
from models.model import Model


class Event(BaseModel):
    home_team: str
    away_team: str
    type: str
    details: str
    odds: float


class Coupons(BaseModel):
    type: str
    details: str
    odds: float
    stake: float
    advice: str
    events: list[Event]


class CouponsData(Model):
    coupons: list[Coupons]
    global_advice: str
    date_of_match: Optional[str] = None

    @classmethod
    def find_one(cls, database: Database, date_of_match: str):
        if result := database.Coupons.find_one({"date_of_match": date_of_match}):
            # Exclude _id from the result

            return CouponsData(**result)
        else:
            return None

    @classmethod
    def get_extremum_date(cls, database: Database):
        query = [{
            "$group": {
                "_id": None,
                "date_plus_ancienne": {"$min": "$date_of_match"},
                "date_plus_recente": {"$max": "$date_of_match"}
            }
        }
        ]
        result = database.Coupons.aggregate(query)
        return next(result)

    @classmethod
    def find_one_or_404(cls, database: Database, date_of_match: str):
        if result := cls.find_one(database, date_of_match):
            return result
        else:
            # nOT FOUND EXCEPTION
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé",
            )

    def save_or_update(self):
        data = self.to_bson()
        if self.database.Coupons.find_one({"date_of_match": self.date_of_match}):
            self.database.Coupons.update_one({"date_of_match": self.date_of_match}, {"$set": data})
        else:
            result = self.database.Coupons.insert_one(data)
            self.id = PydanticObjectId(result.inserted_id)

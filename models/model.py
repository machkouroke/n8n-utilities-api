import inspect
from typing import Optional, Any

from pydantic import BaseModel, Field
from datetime import date, datetime

from dependencies.objectid import PydanticObjectId


class Model(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    database: Optional[Any] = None

    def model_dump(self, *args, **kwargs):

        kwargs["exclude"] = (kwargs.get("exclude", set()) or set()) | {"database"}
        return super().model_dump(*args, **kwargs)


    def set_db(self, database):
        self.database = database

    def to_bson(self, to_exclude=None):
        if to_exclude is None:
            to_exclude = set()
        to_exclude.add("database")
        data = self.dict(by_alias=True, exclude=to_exclude)
        if "_id" in data and data["_id"] is None:
            data.pop("_id")
        return data

""" Stuff for handling MongoDB specifics"""

from typing import Dict, List

from bson.objectid import ObjectId
from pydantic import BaseSettings
from pymongo import MongoClient
from wof.domain.model import WorkoutSession

### Later check out https://github.com/art049/odmantic MongoDB ODM on top of pydantic

# could go to config later
class MongoSettings(BaseSettings):
    host: str = "localhost"
    port: int = 27017
    database: str = "test_db"


class MongoSession:
    def __init__(self) -> None:
        self._mongo_settings = MongoSettings()
        self._client = MongoClient(self._mongo_settings.host, self._mongo_settings.port)
        self._db = self._client[self._mongo_settings.database]
        self._collection = self._db["workout_sessions"]

    def add(self, sessions: List[WorkoutSession]) -> List:
        added_ids = []
        for session in sessions:
            r = self._db["workout_sessions"].insert_one(session.dict())
            added_ids.append(str(r.inserted_id))
        return added_ids

    def get(self, ids: List[str]) -> List[WorkoutSession]:
        result = []
        for _id in ids:
            result.append(
                WorkoutSession(**self._collection.find_one({"_id": ObjectId(_id)}))
            )
        return result

    def list(self) -> List[WorkoutSession]:
        return []

    def commit(self) -> None:
        self.committed = True

    def close(self):
        pass

    def rollback(self):
        pass

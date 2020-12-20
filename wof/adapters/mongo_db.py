""" Stuff for handling MongoDB specifics"""

from typing import List

from bson.objectid import ObjectId
from pymongo import MongoClient
from wof.domain.model import WorkoutSession
from pydantic import BaseSettings

### Later check out https://github.com/art049/odmantic MongoDB ODM on top of pydantic

# could go to config later
class MongoSettings(BaseSettings):
    host: str = "localhost"
    port: int = 27017


class MongoSession:
    def __init__(self) -> None:
        self._mongo_settings = MongoSettings()
        self._client = MongoClient(self._mongo_settings.host, self._mongo_settings.port)

    def add(self, sessions: List[WorkoutSession]) -> None:
        pass

    def get(self, ids: List[str]) -> List[WorkoutSession]:
        return []

    def list(self) -> List[WorkoutSession]:
        return []

    def commit(self) -> None:
        self.committed = True

    def close(self):
        pass

    def rollback(self):
        pass

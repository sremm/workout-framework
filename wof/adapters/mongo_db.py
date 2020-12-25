""" Stuff for handling MongoDB specifics"""

from typing import List, Union

from bson.objectid import ObjectId
from pydantic import BaseSettings
from pymongo import MongoClient
from wof.domain.model import WorkoutSession

### Later check out https://github.com/art049/odmantic MongoDB ODM on top of pydantic

# could go to config later
class MongoSettings(BaseSettings):
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_database: str = "test_db"
    main_collection: str = "workout_sessions"


def mongo_session_factory(mongo_settings: MongoSettings):
    def factory():
        return MongoSession(mongo_settings)

    return factory


class MongoSession:
    def __init__(self, mongo_settings: Union[None, MongoSettings] = None) -> None:
        self._mongo_settings = (
            MongoSettings() if mongo_settings is None else mongo_settings
        )
        self._client = MongoClient(
            self._mongo_settings.mongo_host, self._mongo_settings.mongo_port
        )
        self._db = self._client[self._mongo_settings.mongo_database]
        self._collection = self._db[self._mongo_settings.main_collection]

    def add(self, sessions: List[WorkoutSession]) -> List:
        added_ids = []
        for session in sessions:
            r = self._db[self._mongo_settings.main_collection].insert_one(
                session.dict()
            )
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
        return [WorkoutSession(**x) for x in self._collection.find()]

    def commit(self) -> None:
        self.committed = True

    def close(self):
        self._client.close()

    def rollback(self):
        pass

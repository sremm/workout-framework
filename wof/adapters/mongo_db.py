""" Stuff for handling MongoDB specifics"""

from typing import List, Union, Dict

from bson.objectid import ObjectId
from pydantic import BaseSettings
from config import MongoSettings
from pymongo import MongoClient
from wof.domain.model import WorkoutSession

### Later check out https://github.com/art049/odmantic MongoDB ODM on top of pydantic


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
        # start session and transaction
        self._uncommited: Dict[Dict] = {}
        self._commited: bool = True
        self._db = self._client[self._mongo_settings.mongo_database]
        self._collection = self._db[self._mongo_settings.main_collection]

    def add(self, sessions: List[WorkoutSession]) -> List:
        added_ids = []
        for session in sessions:
            session_dict = session.dict()
            session_dict["_id"] = session_dict["id"]
            self._uncommited[session_dict["_id"]] = session_dict
            added_ids.append(session_dict["_id"])
        self.committed = False
        return added_ids

    def get(self, ids: List[str]) -> List[WorkoutSession]:
        result = []
        for _id in ids:
            document = self._collection.find_one({"_id": ObjectId(_id)})
            if document is None:
                # check if in uncommmitted
                if _id in self._uncommited.keys():
                    result.append(WorkoutSession(**self._uncommited[_id]))
            else:
                result.append(WorkoutSession(**document))

        return result

    def list(self) -> List[WorkoutSession]:
        return [WorkoutSession(**x) for x in self._collection.find()] + [
            WorkoutSession(**x) for x in self._uncommited.values()
        ]

    def commit(self) -> None:
        for session_dict in self._uncommited.values():
            session_dict["_id"] = ObjectId(session_dict["_id"])
            r = self._collection.insert_one(session_dict)
        self.committed = True

    def close(self):
        self._client.close()

    def rollback(self):
        self._uncommited = {}

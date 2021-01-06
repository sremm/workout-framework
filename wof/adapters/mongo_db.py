""" Stuff for handling MongoDB specifics"""

from typing import List, Union, Dict

from bson.objectid import ObjectId
from config import MongoSettings
from pymongo import MongoClient
from wof.domain.model import WorkoutSession, WorkoutSet


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
        self._uncommited_updates: Dict = {}
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

    def update(self, session_id: str, new_sets: List[WorkoutSet]):
        session = self.get([session_id])[0]
        session.add_sets(new_sets)
        session_dict = session.dict()
        self._uncommited_updates[session_id] = {
            "$set": {"sets": session_dict["sets"], "version": session_dict["version"]}
        }

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
        for session_id, update_dict in self._uncommited_updates.items():
            query = {"_id": ObjectId(session_id)}
            self._collection.update_one(query, update_dict)
        self.committed = True

    def close(self):
        self._client.close()

    def rollback(self):
        self._uncommited = {}
        self._uncommited_updates = {}

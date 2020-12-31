from abc import ABC
from typing import List
from wof.adapters.mongo_db import MongoSession

from wof.adapters.csv import CSVSession
from wof.domain.model import WorkoutSession


class BaseWorkoutSessionRepository(ABC):
    def add(self, sessions: List[WorkoutSession]) -> List:
        raise NotImplementedError

    def get(self, ids: List[str]) -> List[WorkoutSession]:
        raise NotImplementedError

    def list(self) -> List[WorkoutSession]:
        raise NotImplementedError


class CSVWorkoutSessionRepository(BaseWorkoutSessionRepository):
    def __init__(self, db_session: CSVSession) -> None:
        self.db_session = db_session

    def add(self, sessions: List[WorkoutSession]) -> None:
        self.db_session.add(sessions)

    def get(self, ids: List[str]) -> List[WorkoutSession]:
        return self.db_session.get(ids)

    def list(self) -> List[WorkoutSession]:
        return self.db_session.list()


class MongoDBWorkoutSessionRepository(BaseWorkoutSessionRepository):
    def __init__(self, db_session: MongoSession) -> None:
        self.db_session = db_session

    def add(self, sessions: List[WorkoutSession]) -> List:
        return self.db_session.add(sessions)

    def get(self, ids: List[str]) -> List[WorkoutSession]:
        return self.db_session.get(ids)

    def list(self) -> List[WorkoutSession]:
        return self.db_session.list()

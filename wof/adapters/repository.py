from abc import ABC
from typing import List, Set

from wof.adapters.mongo_db import MongoSession
from wof.domain.model import WorkoutSession, WorkoutSet


class BaseWorkoutSessionRepository(ABC):
    def __init__(self) -> None:
        self.seen: Set[WorkoutSession] = set()

    def add(self, sessions: List[WorkoutSession]) -> List:
        added_session_ids = self._add(sessions)
        for session in sessions:
            self.seen.add(session)
        return added_session_ids

    def _add(self, sessions: List[WorkoutSession]) -> List:
        raise NotImplementedError

    def get(self, ids: List[str]) -> List[WorkoutSession]:
        sessions = self._get(ids)
        for session in sessions:
            self.seen.add(session)
        return sessions

    def _get(self, ids: List[str]) -> List[WorkoutSession]:
        raise NotImplementedError

    def list(self) -> List[WorkoutSession]:
        raise NotImplementedError

    def update(self, session_id: str, new_sets: List[WorkoutSet]) -> WorkoutSession:
        updated_session = self._update(session_id, new_sets)
        self.seen.add(updated_session)
        return updated_session

    def _update(self, session_id: str, new_sets: List[WorkoutSet]) -> WorkoutSession:
        raise NotImplementedError


class MongoDBWorkoutSessionRepository(BaseWorkoutSessionRepository):
    def __init__(self, db_session: MongoSession) -> None:
        super().__init__()
        self.db_session = db_session

    def _add(self, sessions: List[WorkoutSession]) -> List:
        return self.db_session.add(sessions)

    def _get(self, ids: List[str]) -> List[WorkoutSession]:
        return self.db_session.get(ids)

    def list(self) -> List[WorkoutSession]:
        return self.db_session.list()

    def _update(self, session_id: str, new_sets: List[WorkoutSet]) -> WorkoutSession:
        return self.db_session.update(session_id, new_sets)

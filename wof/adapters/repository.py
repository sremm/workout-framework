from abc import ABC
from typing import List

from wof.adapters.csv import CSVSession
from wof.domain.model import WorkoutSession


class BaseRepository(ABC):
    def add(self, sessions: List[WorkoutSession]) -> None:
        raise NotImplementedError

    def get(self, ids: List[str]) -> List[WorkoutSession]:
        raise NotImplementedError

    def list(self) -> List[WorkoutSession]:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError


class CSVRepository(BaseRepository):
    def __init__(self, session: CSVSession) -> None:
        self.session = session

    def add(self, sessions: List[WorkoutSession]) -> None:
        self.session.add(sessions)

    def get(self, ids: List[str]) -> List[WorkoutSession]:
        return self.session.get(ids)

    def list(self) -> List[WorkoutSession]:
        return self.session.list()

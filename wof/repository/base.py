from abc import ABC
from typing import List, Set
from uuid import UUID

from wof.domain.model import WorkoutSession


class BaseRepository(ABC):
    committed = False

    def add(self, sessions: List[WorkoutSession]) -> None:
        raise NotImplementedError

    def get(self, ids: List[UUID]) -> List[WorkoutSession]:
        raise NotImplementedError

    def list(self) -> List[WorkoutSession]:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError


class FakeRepository(BaseRepository):
    def __init__(self) -> None:
        self._data: List[WorkoutSession] = []

    def add(self, sessions: List[WorkoutSession]) -> None:
        self.committed = False
        return self._data.extend(sessions)

    def get(self, ids: List[UUID]) -> List[WorkoutSession]:
        return [x for x in self._data if x.id in ids]

    def list(self) -> List[WorkoutSession]:
        return list(self._data)

    def commit(self):
        self.committed = True

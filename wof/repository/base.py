from abc import ABC
from typing import List, Set
from uuid import UUID

from wof.domain.model import Session


class BaseRepository(ABC):
    def add(self, sessions: List[Session]) -> None:
        raise NotImplementedError

    def get(self, ids: List[UUID]) -> List[Session]:
        raise NotImplementedError

    def list(self) -> List[Session]:
        raise NotImplementedError


class FakeRepository(BaseRepository):
    def __init__(self) -> None:
        self._data: Set[Session] = set()

    def add(self, sessions: List[Session]) -> None:
        return self._data.update(sessions)

    def get(self, ids: List[UUID]) -> List[Session]:
        return [x for x in self._data if x.id in ids]

    def list(self) -> List[Session]:
        return list(self._data)

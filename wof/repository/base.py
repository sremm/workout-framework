from abc import ABC
from uuid import UUID
from wof.domain.model import Session
from typing import List


class BaseRepository(ABC):
    def add(self, sessions: List[Session]) -> None:
        raise NotImplementedError

    def get(self, ids: List[UUID]) -> List[Session]:
        raise NotImplementedError

    def list(self) -> List[Session]:
        raise NotImplementedError
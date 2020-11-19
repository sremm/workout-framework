from abc import ABC
from wof.domain.types import Session
from typing import List


class BaseRepository(ABC):
    def add(self, sessions: List[Session]) -> None:
        raise NotImplementedError
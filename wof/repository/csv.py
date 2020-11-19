from typing import List

from wof.domain.types import Session
from wof.repository.base import BaseRepository


class CSVRepository(BaseRepository):
    def add_sessions(self, sessions: List[Session]) -> None:
        pass

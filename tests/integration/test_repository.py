from typing import List, Set
from uuid import UUID, uuid4

from wof.domain.types import Session
from wof.repository.base import BaseRepository
from wof.repository.csv import CSVRepository


class FakeRepository(BaseRepository):
    def __init__(self) -> None:
        self._data: Set[Session] = set()

    def add(self, sessions: List[Session]) -> None:
        return self._data.update(sessions)

    def get(self, ids: List[UUID]) -> List[Session]:
        return [x for x in self._data if x.id in ids]

    def list(self) -> List[Session]:
        return list(self._data)


class TestCSVRepository:
    def test_add_and_get(self):
        repository = CSVRepository()
        session_id = uuid4()
        sessions_to_add = [Session(sets=[], id=session_id)]
        repository.add(sessions_to_add)
        session_fetched = repository.get([session_id])
        assert sessions_to_add == session_fetched

    def test_add_and_list(self):
        repository = CSVRepository()
        session_id = uuid4()
        sessions_to_add = [Session(sets=[], id=session_id)]
        repository.add(sessions_to_add)
        all_sessions = repository.list()
        assert sessions_to_add == all_sessions
from typing import List

from wof.adapters import repository
from wof.domain.model import WorkoutSession
from wof.service_layer import services


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


class FakeRepository(repository.BaseRepository):
    def __init__(self, session) -> None:
        self.session = session
        self._data: List[WorkoutSession] = []

    def add(self, sessions: List[WorkoutSession]) -> None:
        self.session.committed = False
        return self._data.extend(sessions)

    def get(self, ids: List[str]) -> List[WorkoutSession]:
        return [x for x in self._data if x.id in ids]

    def list(self) -> List[WorkoutSession]:
        return list(self._data)


def test_allocate_in_batch():
    session = FakeSession()
    repo = FakeRepository(session)
    sessions = [WorkoutSession()]
    services.add_workout_sessions(sessions, repo, session)
    assert len(repo.list()) == 1
    assert session.committed == True

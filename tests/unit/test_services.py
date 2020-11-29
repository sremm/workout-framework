from typing import List

from wof.adapters import repository
from wof.domain.model import WorkoutSession, WorkoutSet
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


def test_add_workout_sessions():
    db_session = FakeSession()
    repo = FakeRepository(db_session)
    sessions = [WorkoutSession()]
    services.add_workout_sessions(sessions, repo, db_session)
    assert len(repo.list()) == 1
    assert db_session.committed == True


def test_add_set_to_existing_session():
    db_session = FakeSession()
    repo = FakeRepository(db_session)
    session_id = "123"
    sessions = [WorkoutSession(id=session_id)]
    services.add_workout_sessions(sessions, repo, db_session)

    sets = [
        WorkoutSet("name", reps=1, weights=0, set_number=1),
        WorkoutSet("name", reps=1, weights=0, set_number=2),
    ]
    services.add_sets_to_workout_session(sets, session_id, repo, db_session)

    fetched_session = repo.get([session_id])[0]
    number_of_sets = len(fetched_session)
    assert number_of_sets == 2

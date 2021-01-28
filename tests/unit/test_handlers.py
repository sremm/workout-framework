from typing import List

from wof.adapters import repository
from wof.domain import events
from wof.domain.model import WorkoutSession, WorkoutSet
from wof.service_layer import handlers, unit_of_work


class FakeRepository(repository.BaseWorkoutSessionRepository):
    def __init__(self) -> None:
        super().__init__()
        self._data: List[WorkoutSession] = []

    def _add(self, sessions: List[WorkoutSession]) -> None:
        return self._data.extend(sessions)

    def _get(self, ids: List[str]) -> List[WorkoutSession]:
        return [x for x in self._data if x.id in ids]

    def list(self) -> List[WorkoutSession]:
        return list(self._data)

    def _update(self, session_id, new_sets: List[WorkoutSet]) -> WorkoutSession:
        session = self.get([session_id])[0]
        session.add_sets(new_sets)
        return session


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self) -> None:
        self.repo = FakeRepository()
        self.committed = False

    def __enter__(self):
        pass

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_workout_sessions():
    uow = FakeUnitOfWork()
    event = events.SessionsToAdd(sessions=[WorkoutSession()])
    handlers.add_workout_sessions(event, uow)
    assert len(uow.repo.list()) == 1
    assert uow.committed == True


def test_add_set_to_existing_session():
    uow = FakeUnitOfWork()
    session = WorkoutSession()
    sessions_event = events.SessionsToAdd(sessions=[session])
    handlers.add_workout_sessions(sessions_event, uow)

    sets = [
        WorkoutSet(exercise="name", reps=1, weights=0, set_number=1),
        WorkoutSet(exercise="name", reps=1, weights=0, set_number=2),
    ]
    sets_event = events.SetsCompleted(session_id=session.id, sets=sets)
    handlers.add_sets_to_workout_session(sets_event, uow)

    fetched_session = handlers.list_all_sessions(uow)[0]
    number_of_sets = len(fetched_session)
    assert number_of_sets == 2

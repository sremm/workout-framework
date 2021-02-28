from typing import List

import pytest
from wof.adapters import repository
from wof.bootstrap import bootstrap_handle
from wof.domain import commands, events
from wof.domain.model import WorkoutSession, WorkoutSet
from wof.service_layer import messagebus, unit_of_work


class FakeRepository(repository.BaseWorkoutSessionRepository):
    def __init__(self) -> None:
        super().__init__()
        self._data: List[WorkoutSession] = []

    def _add(self, sessions: List[WorkoutSession]) -> List:
        self._data.extend(sessions)
        return [x.id for x in sessions]

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


@pytest.fixture
def fake_bus_handle():
    return bootstrap_handle(uow=FakeUnitOfWork())


def test_add_workout_sessions(fake_bus_handle):
    command = commands.AddSessions(sessions=[WorkoutSession()])
    results = fake_bus_handle(command)
    result = results[0]
    assert len(result) == 1


def test_add_set_to_existing_session_and_list_all_session(fake_bus_handle):
    session = WorkoutSession()
    command = commands.AddSessions(sessions=[session])
    fake_bus_handle(command)

    sets = [
        WorkoutSet(exercise="name", reps=1, weights=0, set_number=1),
        WorkoutSet(exercise="name", reps=1, weights=0, set_number=2),
    ]
    command = commands.AddSetsToSession(session_id=session.id, sets=sets)
    result = fake_bus_handle(command)
    added_sets = result[0]

    assert len(added_sets) == 2


def test_polar_import(fake_bus_handle):
    command = commands.ImportSessionsFromPolarData(
        data=[
            {
                "duration": "PT6120S",
                "exercises": [
                    {
                        "duration": "PT6120S",
                        "samples": {},
                        "sport": "GYMNASTICK",
                        "startTime": "2019-12-28T14:05:00.000",
                        "stopTime": "2019-12-28T15:47:00.000",
                        "zones": {},
                    }
                ],
                "exportVersion": "1.3",
                "startTime": "2019-12-28T14:05:00.000",
                "stopTime": "2019-12-28T15:47:00.000",
            }
        ]
    )
    results = fake_bus_handle(command)
    added_ids = results[0]
    assert len(added_ids) == 1


def test_intensity_import(fake_bus_handle):
    assert 0


def test_polar_intensity_merge_import(fake_bus_handle):
    assert 0

from wof.service_layer.unit_of_work import CSVUnitOfWork
from wof.adapters.csv import csv_session_factory
from wof.domain import model
import pytest


@pytest.fixture
def session_factory(tmp_path):
    return csv_session_factory(tmp_path / "test_data.csv")


def test_uow_can_add_workout_sessions(session_factory):
    uow = CSVUnitOfWork(session_factory)
    with uow:
        workout_sessions = [
            model.WorkoutSession(id="abc123", sets=[model.WorkoutSet()])
        ]
        uow.repo.add(workout_sessions)
        uow.commit()
    fetched_session = uow.repo.get(["abc123"])
    assert fetched_session == workout_sessions


def test_rolls_back_uncommited_work_by_default(session_factory):
    uow = CSVUnitOfWork(session_factory)
    with uow:
        workout_sessions = [
            model.WorkoutSession(id="abc123", sets=[model.WorkoutSet()])
        ]
        uow.repo.add(workout_sessions)
    session_list = uow.repo.list()
    assert session_list == []


def test_rolls_back_on_exception(session_factory):
    class MyException(Exception):
        pass

    uow = CSVUnitOfWork(session_factory)
    try:
        with uow:
            workout_sessions = [
                model.WorkoutSession(id="abc123", sets=[model.WorkoutSet()])
            ]
            uow.repo.add(workout_sessions)
            raise MyException()
    except MyException:
        pass

    session_list = uow.repo.list()
    assert session_list == []
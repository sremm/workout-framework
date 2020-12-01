from wof.service_layer.unit_of_work import CSVUnitOfWork
from wof.adapters.csv import csv_session_factory
from wof.domain import model


def test_uow_can_add_workout_sessions(tmp_path):
    dataset_path = tmp_path / "test_data.csv"
    session_factory = csv_session_factory(dataset_path)

    uow = CSVUnitOfWork(session_factory)
    with uow:
        workout_sessions = [
            model.WorkoutSession(id="abc123", sets=[model.WorkoutSet()])
        ]
        uow.repo.add(workout_sessions)
        uow.commit()
    fetched_session = uow.repo.get(["abc123"])
    assert fetched_session == workout_sessions
from wof.repository import base
from wof.service_layer import services
from wof.domain.model import WorkoutSession
from wof.service_layer.unit_of_work import FakeUnitOfWork


def test_allocate_in_batch():
    session = base.FakeSession()
    repo = base.FakeRepository(session)
    sessions = [WorkoutSession()]
    services.add_workout_sessions(sessions, repo, session)
    assert len(repo.list()) == 1
    assert session.committed == True


# def test_allocate_in_batch():
#     uow = FakeUnitOfWork()
#     sessions = [WorkoutSession()]
#     services.add_workout_sessions(sessions, uow)
#     assert uow.committed == True
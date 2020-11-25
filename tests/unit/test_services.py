from wof.repository import base
from wof.service_layer import services
from wof.domain.model import WorkoutSession


def test_allocate_in_batch():
    session = base.FakeSession()
    repo = base.FakeRepository(session)
    sessions = [WorkoutSession()]
    services.allocate_in_batch(sessions, repo, session)
    assert len(repo.list()) == 1
    assert session.committed == True
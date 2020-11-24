from wof.repository.base import FakeRepository
from wof.service_layer import services
from wof.domain.model import Session, WorkoutSet


def test_allocate_in_batch():
    repo = FakeRepository()
    sessions = [Session([WorkoutSet()])]
    services.allocate_in_batch(sessions, repo)
    assert len(repo.list()) == 1
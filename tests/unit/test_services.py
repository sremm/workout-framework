from wof.repository.base import FakeRepository
from wof.service_layer import services
from wof.domain.model import Session


def test_allocate_in_batch():
    repo = FakeRepository()
    sessions = [Session()]
    services.allocate_in_batch(sessions, repo)
    assert len(repo.list()) == 1
    assert repo.committed == True
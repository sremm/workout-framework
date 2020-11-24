from wof.repository.base import FakeRepository
from wof import services


def test_allocate_in_batch():
    repo = FakeRepository()
    sessions = []
    services.allocate_in_batch(sessions, repo)
    assert 1
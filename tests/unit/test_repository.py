from wof.repository.csv import CSVRepository
from wof.domain.types import Session
from uuid import UUID


def test_repository_can_add_and_return_session():
    repository = CSVRepository()
    session_id = UUID("abc")
    session_to_add = Session(sets=[], id=session_id)
    repository.add([session_to_add])
    session_fetched = repository.get([session_id])
    assert session_to_add == session_fetched
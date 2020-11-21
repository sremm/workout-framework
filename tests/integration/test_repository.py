from wof.repository.csv import CSVRepository
from wof.domain.types import Session
from uuid import uuid4


def test_csv_repository_can_add_and_return_session():
    repository = CSVRepository()
    session_id = uuid4()
    sessions_to_add = [Session(sets=[], id=session_id)]
    repository.add(sessions_to_add)
    session_fetched = repository.get([session_id])
    assert sessions_to_add == session_fetched
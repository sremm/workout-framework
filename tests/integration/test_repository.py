from uuid import uuid4

from wof.domain.model import Session, WorkoutSet
from wof.repository.csv import CSVRepository


class TestCSVRepository:
    def test_add_and_get(self):
        repository = CSVRepository()
        session_id = uuid4()
        sessions_to_add = [Session(id=session_id)]
        repository.add(sessions_to_add)
        session_fetched = repository.get([session_id])
        assert sessions_to_add == session_fetched

    def test_add_and_list(self):
        repository = CSVRepository()
        sessions_to_add = [Session()]
        repository.add(sessions_to_add)
        all_sessions = repository.list()
        assert sessions_to_add == all_sessions

    def test_add_save_and_load(self, tmp_path):
        # prep
        path = tmp_path / "data.csv"
        repository = CSVRepository(path)
        sets = [WorkoutSet()]
        sessions = [Session(sets)]
        # add
        repository.add(sessions)
        # save
        repository.commit()
        # load
        new_repository_instance = CSVRepository(path)
        loaded_sessions = new_repository_instance.list()
        assert sessions == loaded_sessions

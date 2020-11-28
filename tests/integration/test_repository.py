from wof.domain.model import WorkoutSession, WorkoutSet
from wof.repository.csv import CSVRepository, CSVSession


class TestCSVRepository:
    def test_add_and_get(self):
        csv_session = CSVSession()
        repository = CSVRepository(csv_session)
        session_id = "abc123"
        sessions_to_add = [WorkoutSession(id=session_id)]
        repository.add(sessions_to_add)
        session_fetched = repository.get([session_id])
        assert sessions_to_add == session_fetched

    def test_add_and_list(self):
        csv_session = CSVSession()
        repository = CSVRepository(csv_session)
        sessions_to_add = [WorkoutSession()]
        repository.add(sessions_to_add)
        all_sessions = repository.list()
        assert sessions_to_add == all_sessions

    def test_add_save_and_load(self, tmp_path):
        # prep
        path = tmp_path / "data.csv"
        csv_session = CSVSession(path)
        repository = CSVRepository(csv_session)
        sets = [WorkoutSet()]
        sessions = [WorkoutSession(sets)]
        # add
        repository.add(sessions)
        # save
        csv_session.commit()
        # load
        new_csv_session = CSVSession(path)
        new_repository_instance = CSVRepository(new_csv_session)
        loaded_sessions = new_repository_instance.list()
        assert sessions == loaded_sessions

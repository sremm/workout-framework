from wof.adapters.mongo_db import MongoSession
from wof.domain.model import WorkoutSession, WorkoutSet
from wof.adapters.repository import CSVWorkoutSessionRepository, CSVSession
from wof.adapters.repository import MongoDBWorkoutSessionRepository
from datetime import datetime


class TestMongoDBRepository:
    def test_add_and_get(self):
        mongo_session = MongoSession()
        repository = MongoDBWorkoutSessionRepository(mongo_session)
        session_id = "abc123"
        sessions_to_add = [WorkoutSession(id=session_id)]
        added_session_ids = repository.add(sessions_to_add)
        session_fetched = repository.get(added_session_ids)
        # truncate time since mongo db does that
        sessions_to_add[0].start_time = datetime.strptime(
            str(sessions_to_add[0].start_time)[:-3], "%Y-%m-%d %H:%M:%S.%f"
        )
        assert sessions_to_add == session_fetched

    def test_add_and_list(self):
        mongo_session = MongoSession()
        repository = MongoDBWorkoutSessionRepository(mongo_session)
        sessions_to_add = [WorkoutSession()]
        repository.add(sessions_to_add)
        all_sessions = repository.list()
        assert sessions_to_add == all_sessions

    def test_add_save_and_load(self):
        #
        mongo_session = MongoSession()
        repository = MongoDBWorkoutSessionRepository(mongo_session)
        sets = [WorkoutSet()]
        sessions = [WorkoutSession(sets=sets)]
        # add
        repository.add(sessions)
        # save
        mongo_session.commit()
        # close session?
        # repopen session?
        # load
        new_mongo_session = MongoSession()
        new_repository_instance = MongoDBWorkoutSessionRepository(new_mongo_session)
        loaded_sessions = new_repository_instance.list()
        assert sessions == loaded_sessions


class TestCSVRepository:
    def test_add_and_get(self):
        csv_session = CSVSession()
        repository = CSVWorkoutSessionRepository(csv_session)
        session_id = "abc123"
        sessions_to_add = [WorkoutSession(id=session_id)]
        repository.add(sessions_to_add)
        session_fetched = repository.get([session_id])
        assert sessions_to_add == session_fetched

    def test_add_and_list(self):
        csv_session = CSVSession()
        repository = CSVWorkoutSessionRepository(csv_session)
        sessions_to_add = [WorkoutSession()]
        repository.add(sessions_to_add)
        all_sessions = repository.list()
        assert sessions_to_add == all_sessions

    def test_add_save_and_load(self, tmp_path):
        # prep
        path = tmp_path / "data.csv"
        csv_session = CSVSession(path)
        repository = CSVWorkoutSessionRepository(csv_session)
        sets = [WorkoutSet()]
        sessions = [WorkoutSession(sets=sets)]
        # add
        repository.add(sessions)
        # save
        csv_session.commit()
        # load
        new_csv_session = CSVSession(path)
        new_repository_instance = CSVWorkoutSessionRepository(new_csv_session)
        loaded_sessions = new_repository_instance.list()
        assert sessions == loaded_sessions

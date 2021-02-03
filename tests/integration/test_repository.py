from datetime import datetime

from wof.adapters.mongo_db import MongoSession
from wof.adapters.repository import (
    MongoDBWorkoutSessionRepository,
)
from wof.domain.model import TimeSeries, WorkoutSession, WorkoutSet


def create_timeseries_entry() -> TimeSeries:
    time = [
        datetime(2000, 1, 1, 15, 0, 0, 0),
        datetime(2000, 1, 1, 15, 0, 1, 0),
        datetime(2000, 1, 1, 15, 0, 2, 0),
    ]
    return TimeSeries(values=[1, 2, 3], time=time, unit="bpm")


class TestMongoDBRepository:
    def test_add_and_get(self, mongo_test_db):
        # connect to db
        mongo_session = MongoSession()
        repository = MongoDBWorkoutSessionRepository(mongo_session)
        # populate with desired values
        workout_session = WorkoutSession()
        workout_session.start_time = datetime.strptime(
            str(workout_session.start_time)[:-3], "%Y-%m-%d %H:%M:%S.%f"
        )  # since mongodb truncates to milliseconds from microseconds

        workout_session.update_heart_rate(create_timeseries_entry())
        sessions_to_add = [workout_session]

        # add to db
        added_session_ids = repository.add(sessions_to_add)
        # get for db
        session_fetched = repository.get(added_session_ids)
        assert sessions_to_add == session_fetched

    def test_add_and_list(self, mongo_test_db):
        mongo_session = MongoSession()
        repository = MongoDBWorkoutSessionRepository(mongo_session)
        sessions_to_add = [WorkoutSession()]
        repository.add(sessions_to_add)
        all_sessions = repository.list()
        assert sessions_to_add == all_sessions

    def test_add_save_and_load(self, mongo_test_db):
        #
        mongo_session = MongoSession()
        repository = MongoDBWorkoutSessionRepository(mongo_session)
        sets = [WorkoutSet()]
        sessions = [WorkoutSession(sets=sets)]
        sessions[0].start_time = datetime.strptime(
            str(sessions[0].start_time)[:-3], "%Y-%m-%d %H:%M:%S.%f"
        )
        # add
        repository.add(sessions)
        # save
        mongo_session.commit()
        mongo_session.close()
        # repopen session?
        new_mongo_session = MongoSession()
        new_repository_instance = MongoDBWorkoutSessionRepository(new_mongo_session)
        loaded_sessions = new_repository_instance.list()
        assert sessions == loaded_sessions

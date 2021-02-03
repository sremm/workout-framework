from wof.domain.model import WorkoutSession, DateTimeRange
from wof.domain import commands, views
from wof.service_layer import messagebus
from datetime import datetime
from wof.service_layer.unit_of_work import MongoUnitOfWork


def test_workout_sessions_view(mongo_session_factory_instance):
    # add three sessions
    command = commands.AddSessions(
        sessions=[
            WorkoutSession(start_time=datetime(2020, 1, 1, 12)),
            WorkoutSession(start_time=datetime(2020, 1, 2, 17)),
            WorkoutSession(start_time=datetime(2020, 1, 3, 15)),
        ]
    )
    uow = MongoUnitOfWork(mongo_session_factory_instance)
    messagebus.handle(command, uow)

    # create daterange to include only 1
    datetime_range = DateTimeRange(
        start=datetime(2020, 1, 2, 0), end=datetime(2020, 1, 3, 0)
    )
    results = views.workout_sessions(datetime_range, uow)
    del results[0]["id"]
    del results[0]["_id"]
    assert results == [
        {
            "sets": [],
            "start_time": datetime(2020, 1, 2, 17),
            "stop_time": None,
            "heart_rate": None,
            "version": 1,
            "events": [],
            "origin": [],
        }
    ]

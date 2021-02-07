from datetime import datetime

import pytest
from wof.bootstrap import bootstrap_handle
from wof.domain import commands, views
from wof.domain.model import DateTimeRange, WorkoutSession
from wof.service_layer import messagebus
from wof.service_layer.unit_of_work import MongoUnitOfWork


@pytest.fixture
def mongo_bus_handle(mongo_session_factory_instance):
    uow = MongoUnitOfWork(mongo_session_factory_instance)
    return bootstrap_handle(uow)


def test_workout_sessions_view(mongo_bus_handle):
    # add three sessions
    command = commands.AddSessions(
        sessions=[
            WorkoutSession(start_time=datetime(2020, 1, 1, 12)),
            WorkoutSession(start_time=datetime(2020, 1, 2, 17)),
            WorkoutSession(start_time=datetime(2020, 1, 3, 15)),
        ]
    )
    mongo_bus_handle(command)

    # create daterange to include only 1
    datetime_range = DateTimeRange(
        start=datetime(2020, 1, 2, 0), end=datetime(2020, 1, 3, 0)
    )
    command = commands.GetSessions(date_range=datetime_range)
    results = mongo_bus_handle(command)
    result = results[0]
    del result[0]["id"]
    del result[0]["_id"]
    assert result == [
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

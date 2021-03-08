from datetime import datetime
from typing import List

import pytest
from wof.bootstrap import bootstrap_handle
from wof.domain import commands, views
from wof.domain.model import DateTimeRange, TimeSeries, WorkoutSession, WorkoutSet
from wof.service_layer import messagebus
from wof.service_layer.unit_of_work import MongoUnitOfWork


@pytest.fixture
def mongo_bus_handle(mongo_session_factory_instance):
    uow = MongoUnitOfWork(mongo_session_factory_instance)
    return bootstrap_handle(uow)


def test_workout_sessions_summary_view(mongo_bus_handle):
    # add three sessions
    time: List[datetime] = [
        datetime(2000, 1, 1, 15, 0, 0, 0),
        datetime(2000, 1, 1, 15, 0, 1, 0),
        datetime(2000, 1, 1, 15, 0, 2, 0),
    ]
    hr_data = TimeSeries(values=[141, 142], time=time, unit="bpm")
    command = commands.AddSessions(
        sessions=[
            WorkoutSession(
                start_time=datetime(2020, 1, 1, 12), heart_rate=hr_data, sets=[WorkoutSet(reps=1, weights=10)]
            ),
            WorkoutSession(
                start_time=datetime(2020, 1, 2, 17), heart_rate=hr_data, sets=[WorkoutSet(reps=1, weights=10)]
            ),
            WorkoutSession(
                start_time=datetime(2020, 1, 3, 15), heart_rate=hr_data, sets=[WorkoutSet(reps=1, weights=10)]
            ),
        ]
    )
    mongo_bus_handle(command)

    # create daterange to include only 1
    datetime_range = DateTimeRange(start=datetime(2020, 1, 2, 0), end=datetime(2020, 1, 3, 0))
    command = commands.GetWorkoutSessionSummary(date_range=datetime_range)
    results = mongo_bus_handle(command)
    result_dict = results[0].dict()
    assert len(result_dict["session_ids"]) == 1, "Summary was not created from exactly one session"
    del result_dict["session_ids"]
    assert result_dict == {
        "workout_set_stats": {"exercises": ("name",), "total_reps": 1, "total_weight": 10, "weight_unit": "kg"},
        "heart_rate_stats": {"max": 142.0, "mean": 141.5, "min": 141.0, "std": 0.5},
    }

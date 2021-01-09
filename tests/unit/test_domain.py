from datetime import datetime
from wof.domain.model import TimeSeries, WorkoutSession
from wof.domain.model import WorkoutSet
from wof.domain import events
from typing import List


def test_add_sets_to_session():
    session = WorkoutSession()
    sets = [WorkoutSet(), WorkoutSet()]
    session.add_sets(sets)
    assert len(session) == 2


def test_create_set_with_multiple_exercises():
    a_set = WorkoutSet(
        exercise=["first", "second"],
    )
    assert len(a_set) == 2


def test_create_session_with_hr_data():
    session = WorkoutSession()

    time: List[datetime] = [
        datetime(2000, 1, 1, 15, 0, 0, 0),
        datetime(2000, 1, 1, 15, 0, 1, 0),
        datetime(2000, 1, 1, 15, 0, 2, 0),
    ]
    hr_data = TimeSeries(values=[1, 2, 3], time=time, unit="bpm")
    session.update_heart_rate(hr_data)

    assert session.heart_rate == hr_data


def test_event_raised_when_adding_many_sets_to_a_workout_session():
    session = WorkoutSession()
    sets = [WorkoutSet() for _ in range(10)]
    session.add_sets(sets)
    assert len(session.events) == 1, "Events empty but should have 1 etry"
    assert session.events[-1] == events.ManySetsAddedToWorkoutSession(
        workout_session_id=session.id, number_of_sets_added=10
    )

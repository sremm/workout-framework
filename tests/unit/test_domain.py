from datetime import datetime
from typing import List

from wof.domain.model import TimeSeries, WorkoutSession, WorkoutSet


class TestWorkoutSet:
    def test_create_with_multiple_exercises(self):
        a_set = WorkoutSet(
            exercise=["first", "second"],
        )
        assert len(a_set) == 2


class TestWorkoutSession:
    def test_create_with_hr_data(self):
        session = WorkoutSession()

        time: List[datetime] = [
            datetime(2000, 1, 1, 15, 0, 0, 0),
            datetime(2000, 1, 1, 15, 0, 1, 0),
            datetime(2000, 1, 1, 15, 0, 2, 0),
        ]
        hr_data = TimeSeries(values=[1, 2, 3], time=time, unit="bpm")
        session.update_heart_rate(hr_data)

        assert session.heart_rate == hr_data

    def test_add_sets(self):
        session = WorkoutSession()
        sets = [WorkoutSet(), WorkoutSet()]
        session.add_sets(sets)
        assert len(session) == 2

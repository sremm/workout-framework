from datetime import datetime
from typing import List

import numpy as np
from wof.domain.analytics import (
    TimeSeriesStats,
    WorkoutSessionsSummary,
    WorkoutSetStats,
    compute_time_series_stats,
    compute_workout_sessions_summary,
)
from wof.domain.model import TimeSeries, WorkoutSession, WorkoutSet


class TestWorkoutSessionSummary:
    def test_from_one_session(self):
        sets = [WorkoutSet(exercise="one", reps=5, weights=10, set_number=x) for x in range(1, 4)]
        time: List[datetime] = [
            datetime(2000, 1, 1, 15, 0, 0, 0),
            datetime(2000, 1, 1, 15, 0, 1, 0),
            datetime(2000, 1, 1, 15, 0, 2, 0),
        ]
        hr_data = TimeSeries(values=[141, 142], time=time, unit="bpm")
        workout_sessions = [WorkoutSession(sets=sets, heart_rate=hr_data)]
        summary = compute_workout_sessions_summary(workout_sessions)
        assert summary == WorkoutSessionsSummary(
            session_ids=[workout_sessions[0].id],
            workout_set_stats=WorkoutSetStats(total_reps=15, total_weight=150.0, exercises=("one",)),
            heart_rate_stats=TimeSeriesStats(mean=141.5, min=141.0, max=142.0, std=0.5),
        )

    def test_from_no_sessions(self):
        summary = compute_workout_sessions_summary([])
        assert summary == WorkoutSessionsSummary(
            session_ids=[],
            workout_set_stats=WorkoutSetStats(total_reps=0, total_weight=0, exercises=()),
            heart_rate_stats=TimeSeriesStats(mean=np.nan, min=np.nan, max=np.nan, std=np.nan),
        )


class TestTimeSeriesStats:
    def test_compute_from_single_series(self):
        time: List[datetime] = [
            datetime(2000, 1, 1, 15, 0, 0, 0),
            datetime(2000, 1, 1, 15, 0, 1, 0),
        ]
        data = TimeSeries(values=[1, 2], time=time, unit="bpm")
        results = TimeSeriesStats.compute(data)
        assert results == TimeSeriesStats(mean=1.5, min=1.0, max=2.0, std=0.5)

    def test_compute_from_multiple_series(self):
        time: List[datetime] = [
            datetime(2000, 1, 1, 15, 0, 0, 0),
            datetime(2000, 1, 1, 15, 0, 1, 0),
        ]
        series1 = TimeSeries(values=[1, 2], time=time, unit="bpm")
        series2 = TimeSeries(values=[5, 10], time=time, unit="bpm")
        results = compute_time_series_stats([series1, series2])
        assert results == TimeSeriesStats(mean=4.5, min=3.0, max=6, std=1.5)


class TestWorkoutSetStats:
    def test_adding_two_stats(self):
        result = WorkoutSetStats(exercises=("one",), total_reps=1, total_weight=1,) + WorkoutSetStats(
            exercises=("one",),
            total_reps=1,
            total_weight=1,
        )
        assert result == WorkoutSetStats(
            exercises=("one",),
            total_reps=2,
            total_weight=2,
        )

    def test_adding_set_with_multiple_exercises(self):
        result = WorkoutSetStats(exercises=("one", "two"), total_reps=2, total_weight=2,) + WorkoutSetStats(
            exercises=("three", "four"),
            total_reps=2,
            total_weight=2,
        )
        assert result == WorkoutSetStats(
            exercises=("four", "one", "three", "two"),
            total_reps=4,
            total_weight=4,
        )

    def test_cannot_add_with_other_types(self):
        raised = None
        try:
            WorkoutSetStats(
                exercises=("one",),
                total_reps=1,
                total_weight=1,
            ) + 2
        except TypeError as e:
            raised = e
        assert raised is not None
        assert "Addition of" in raised.args[0] and "<class 'int'> not allowed" in raised.args[0]

    def test_compute_from_workout_sets(self):
        sets = [WorkoutSet(exercise="one", reps=5, weights=10, set_number=x) for x in range(1, 4)] + [
            WorkoutSet(exercise=["two", "three"], reps=[5, 5], weights=[10, 10], set_number=4)
        ]
        result = WorkoutSetStats.compute(sets)
        assert result == WorkoutSetStats(total_reps=25, total_weight=250, exercises=("one", "three", "two"))

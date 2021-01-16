from datetime import datetime
from typing import List

from wof.domain.analytics import (
    compute_time_series_stats,
    compute_workout_sessions_summary,
)
from wof.domain.model import (
    TimeSeries,
    TimeSeriesStats,
    WorkoutSession,
    WorkoutSessionsSummary,
    WorkoutSet,
    WorkoutSetStats,
)


def test_compute_time_series_stats():
    time: List[datetime] = [
        datetime(2000, 1, 1, 15, 0, 0, 0),
        datetime(2000, 1, 1, 15, 0, 1, 0),
    ]
    series1 = TimeSeries(values=[1, 2], time=time, unit="bpm")
    series2 = TimeSeries(values=[5, 10], time=time, unit="bpm")
    results = compute_time_series_stats([series1, series2])
    assert results == TimeSeriesStats(mean=4.5, min=3.0, max=6, std=1.5)


def test_workout_session_summary_from_one_session():
    sets = [
        WorkoutSet(exercise="one", reps=5, weights=10, set_number=x)
        for x in range(1, 4)
    ]
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
        workout_set_stats=WorkoutSetStats(
            total_reps=15, total_weight=150.0, exercises=("one",)
        ),
        heart_rate_stats=TimeSeriesStats(mean=141.5, min=141.0, max=142.0, std=0.5),
    )

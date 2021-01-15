from datetime import datetime
from typing import List

from wof.domain.analytics import compute_workout_sessions_summary
from wof.domain.model import (
    TimeSeries,
    TimeSeriesStats,
    WorkoutSession,
    WorkoutSessionsSummary,
    WorkoutSet,
    WorkoutSetStats,
)


def test_workout_session_summary_from_one_session():
    sets = [
        WorkoutSet(exercise="one", reps=5, weight=10, set_number=x) for x in range(1, 4)
    ]
    time: List[datetime] = [
        datetime(2000, 1, 1, 15, 0, 0, 0),
        datetime(2000, 1, 1, 15, 0, 1, 0),
        datetime(2000, 1, 1, 15, 0, 2, 0),
    ]
    hr_data = TimeSeries(values=[140, 141, 142], time=time, unit="bpm")
    workout_sessions = [WorkoutSession(sets=sets, heart_rate=hr_data)]
    summary = compute_workout_sessions_summary(workout_sessions)
    assert summary == WorkoutSessionsSummary(
        session_ids=[workout_sessions[0].id],
        workout_set_stats=WorkoutSetStats(
            total_reps=15, total_weight_lifted=150.0, exercise=("one",)
        ),
        heart_rate_stats=TimeSeriesStats(mean=141.0, min=140.0, max=141.0, std=1.0),
    )

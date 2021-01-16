from wof.domain.model import (
    TimeSeries,
    TimeSeriesStats,
    WorkoutSession,
    WorkoutSessionsSummary,
    WorkoutSetStats,
)
from typing import List
import numpy as np


def compute_time_series_stats(data: List[TimeSeries]) -> TimeSeriesStats:
    stats_mean = np.mean([TimeSeriesStats.compute(x).values for x in data], axis=0)
    return TimeSeriesStats(
        mean=stats_mean[0], min=stats_mean[1], max=stats_mean[2], std=stats_mean[3]
    )


def compute_merged_set_stats(
    sessions: List[WorkoutSession],
) -> WorkoutSetStats:
    stats: List[WorkoutSetStats] = [
        WorkoutSetStats.compute(session.sets) for session in sessions
    ]
    result: WorkoutSetStats = sum(stats, start=WorkoutSetStats.empty_stats())
    return result


def compute_workout_sessions_summary(
    sessions: List[WorkoutSession],
) -> WorkoutSessionsSummary:
    return WorkoutSessionsSummary(
        session_ids=[x.id for x in sessions],
        workout_set_stats=compute_merged_set_stats(sessions),
        heart_rate_stats=compute_time_series_stats(
            [x.heart_rate for x in sessions if x.heart_rate is not None]
        ),
    )

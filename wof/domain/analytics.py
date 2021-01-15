from wof.domain import model
from typing import List


def compute_time_series_stats(data: List[model.TimeSeries]) -> model.TimeSeriesStats:

    return model.TimeSeriesStats(mean=1, min=2, max=3, std=1.0)


def compute_merged_set_stats(
    sessions: List[model.WorkoutSession],
) -> model.WorkoutSetStats:
    stats: List[model.WorkoutSetStats] = [
        model.WorkoutSetStats.calculate(session.sets) for session in sessions
    ]
    result: model.WorkoutSetStats = sum(stats)
    return result


def compute_workout_sessions_summary(
    sessions: List[model.WorkoutSession],
) -> model.WorkoutSessionsSummary:
    return model.WorkoutSessionsSummary(
        session_ids=[x.id for x in sessions],
        workout_set_stats=compute_merged_set_stats(sessions),
        heart_rate_stats=compute_time_series_stats(
            [x.heart_rate for x in sessions if x.heart_rate is not None]
        ),
    )

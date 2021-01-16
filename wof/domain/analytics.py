from typing import List, Tuple

import numpy as np
from pydantic import BaseModel
from wof.domain.model import TimeSeries, WorkoutSession, WorkoutSet


class WorkoutSetStats(BaseModel):
    total_reps: int
    total_weight: int
    exercises: Tuple[str, ...]
    weight_unit: str = "kg"

    @staticmethod
    def compute(sets: List[WorkoutSet]):
        def _compute_stats(workout_set: WorkoutSet):
            if workout_set.has_subsets:
                return WorkoutSetStats(
                    total_reps=np.sum(workout_set.reps),
                    total_weight=np.sum(
                        np.array(workout_set.weights) * np.array(workout_set.reps)
                    ),
                    exercises=tuple(sorted(set(workout_set.exercise))),
                )
            else:
                return WorkoutSetStats(
                    total_reps=workout_set.reps,
                    total_weight=workout_set.weights * workout_set.reps,
                    exercises=(workout_set.exercise,),
                )

        stats_list = [_compute_stats(x) for x in sets]
        return sum(stats_list, start=WorkoutSetStats.empty_stats())

    @staticmethod
    def empty_stats():
        return WorkoutSetStats(total_reps=0, total_weight=0, exercises=())

    def __add__(self, other):
        if type(other) != type(self):
            raise TypeError(f"Addition of {type(self)} and {type(other)} not allowed")
        return WorkoutSetStats(
            total_reps=self.total_reps + other.total_reps,
            total_weight=self.total_weight + other.total_weight,
            exercises=tuple(sorted(set(self.exercises + other.exercises))),
        )


class TimeSeriesStats(BaseModel):
    """Stats are calculated per series"""

    mean: float
    min: float
    max: float
    std: float

    @staticmethod
    def compute(time_series: TimeSeries):
        return TimeSeriesStats(
            mean=np.nanmean(time_series.values),
            min=min(time_series.values),
            max=max(time_series.values),
            std=np.nanstd(time_series.values),
        )

    @property
    def values(self) -> np.ndarray:
        return np.array(
            [
                self.mean,
                self.min,
                self.max,
                self.std,
            ]
        )


class WorkoutSessionsSummary(BaseModel):
    session_ids: Tuple[str, ...]
    workout_set_stats: WorkoutSetStats
    heart_rate_stats: TimeSeriesStats


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

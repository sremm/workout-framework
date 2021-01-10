from wof.domain import model
from typing import List


def compute_workout_sessions_summary(
    sessions: List[model.WorkoutSession],
) -> model.WorkoutSessionsSummary:
    # do calculations
    return model.WorkoutSessionsSummary()

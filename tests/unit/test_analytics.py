from wof.domain.model import WorkoutSession
from wof.domain.analytics import compute_workout_sessions_summary


def test_workout_session_summary():
    workout_sessions = []
    summary = compute_workout_sessions_summary(workout_sessions)
    assert 0
from datetime import datetime
from typing import List, Dict, Tuple

from wof.domain.model import WorkoutSession


def add_sets_from_sessions(
    base_session: WorkoutSession, sessions_with_sets: List[WorkoutSession]
) -> WorkoutSession:
    result = base_session
    for session in sessions_with_sets:
        result.add_sets(session.sets, origin=session.origin)
    return result


def merge_polar_and_instensity_imports(
    polar_sessions: List[WorkoutSession], intensity_sessions: List[WorkoutSession]
) -> List[WorkoutSession]:
    def _get_start_time_to_session_mapping(
        sessions: List[WorkoutSession],
    ) -> Dict[datetime, WorkoutSession]:
        return {x.start_time: x for x in sessions}

    def _match_datetime_days(
        times_1: List[datetime], times_2: List[datetime]
    ) -> List[Tuple[datetime, datetime]]:
        return [(datetime.now(), datetime.now())]

    polar: Dict = _get_start_time_to_session_mapping(polar_sessions)
    intensity: Dict = _get_start_time_to_session_mapping(intensity_sessions)
    results = []
    return results

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


def are_on_same_day(time_1: datetime, time_2: datetime) -> bool:
    def _as_ymd(d: datetime) -> Tuple[int, int, int]:
        return (d.year, d.month, d.day)

    return _as_ymd(time_1) == _as_ymd(time_2)


def merge_polar_and_instensity_imports(
    polar_sessions: List[WorkoutSession], intensity_sessions: List[WorkoutSession]
) -> List[WorkoutSession]:
    def _get_start_time_to_session_mapping(
        sessions: List[WorkoutSession],
    ) -> Dict[datetime, WorkoutSession]:
        return {x.start_time: x for x in sessions}

    def _match_datetime_days(
        times_1: List[datetime], times_2: List[datetime]
    ) -> List[List[datetime]]:
        result = []
        matched = []
        for time_1 in times_1:
            found_match = False
            for time_2 in times_2:
                if time_2 not in matched and are_on_same_day(time_1, time_2):
                    found_match = True
                    result.append([time_1, time_2])
                    matched.append(time_2)
            if not found_match:
                result.append([time_1])
        return result

    polar: Dict = _get_start_time_to_session_mapping(polar_sessions)
    intensity: Dict = _get_start_time_to_session_mapping(intensity_sessions)
    matched_start_times = _match_datetime_days(
        list(polar.keys()), list(intensity.keys())
    )
    results = []
    for matched_times in matched_start_times:
        base_session = polar[matched_times.pop(0)]
        sessions = [intensity[x] for x in matched_times]
        results.append(add_sets_from_sessions(base_session, sessions))
    return results

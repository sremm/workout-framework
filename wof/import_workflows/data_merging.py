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
    ) -> Tuple[List[List[datetime]], List[datetime], List[datetime]]:
        matched_start_times = []
        umatched_times_1 = []
        umatched_times_2 = []
        matched_times_2 = []
        # find matches for time_1
        for time_1 in times_1:
            found_match = False
            # see if any time_2 matches time_1
            for time_2 in times_2:
                if time_2 not in matched_times_2 and are_on_same_day(time_1, time_2):
                    found_match = True
                    matched_start_times.append([time_1, time_2])
                    matched_times_2.append(time_2)
            if not found_match:
                umatched_times_1.append(time_1)
        # add all times 2 without match to result list
        for time_2 in times_2:
            if time_2 not in matched_times_2:
                umatched_times_2.append(time_2)

        return matched_start_times, umatched_times_1, umatched_times_2

    polar: Dict = _get_start_time_to_session_mapping(polar_sessions)
    intensity: Dict = _get_start_time_to_session_mapping(intensity_sessions)
    (
        matched_start_times,
        unmatched_polar_times,
        unmatched_intensity_times,
    ) = _match_datetime_days(list(polar.keys()), list(intensity.keys()))
    results = []
    for matched_times in matched_start_times:
        base_session = polar[matched_times.pop(0)]
        sessions = [intensity[x] for x in matched_times]
        results.append(add_sets_from_sessions(base_session, sessions))
    for time in unmatched_polar_times:
        results.append(polar[time])
    for time in unmatched_intensity_times:
        results.append(intensity[time])
    return results

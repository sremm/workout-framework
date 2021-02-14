from datetime import datetime
from typing import List, Dict, Tuple

from pydantic import BaseModel
from wof.domain.model import WorkoutSession

import copy


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


class PotentialDatetimeMatches(BaseModel):
    match_base: datetime
    matches: List[datetime]


class PotentialMatchingResult(BaseModel):
    potential_matches: List[PotentialDatetimeMatches]
    unmatched_1: List[datetime]
    unmatched_2: List[datetime]


class FinalMatchingResult(BaseModel):
    matches: List[Tuple[datetime, datetime]]
    unmatched_1: List[datetime]
    unmatched_2: List[datetime]


def merge_polar_and_instensity_imports(
    polar_sessions: List[WorkoutSession], intensity_sessions: List[WorkoutSession]
) -> List[WorkoutSession]:
    def _get_start_time_to_session_mapping(
        sessions: List[WorkoutSession],
    ) -> Dict[datetime, WorkoutSession]:
        return {x.start_time: x for x in sessions}

    def _match_datetime_days(
        times_1: List[datetime], times_2: List[datetime]
    ) -> PotentialMatchingResult:
        """ Datetime based matching """
        matched_start_times = []
        umatched_times_1 = []
        umatched_times_2 = []
        matched_times_1 = set()
        for time_2 in times_2:
            current_matches = []
            # find all matches for time_2
            for time_1 in times_1:
                if are_on_same_day(time_1, time_2):
                    current_matches.append(time_1)
                    matched_times_1.add(time_1)
            if current_matches != []:
                matched_start_times.append(
                    PotentialDatetimeMatches(match_base=time_2, matches=current_matches)
                )
            else:
                umatched_times_2.append(time_2)
        # add all times 1 without match to result list
        for time_1 in times_1:
            if time_1 not in matched_times_1:
                umatched_times_1.append(time_1)

        return PotentialMatchingResult(
            potential_matches=matched_start_times,
            unmatched_1=umatched_times_1,
            unmatched_2=umatched_times_2,
        )

    def _match_session_type(
        potential_results: PotentialMatchingResult,
        polar: Dict[datetime, WorkoutSession],
        intensity: Dict[datetime, WorkoutSession],
    ) -> FinalMatchingResult:
        final_matches = []
        unmatched_1 = copy.copy(potential_results.unmatched_1)
        unmatched_2 = copy.copy(potential_results.unmatched_2)
        for potential_matches in potential_results.potential_matches:
            int_session = intensity[potential_matches.match_base]
            polar_sessions = [polar[x] for x in potential_matches.matches]
            polar_matches = []
            for polar_session in polar_sessions:
                if polar_session.type == int_session.type:
                    polar_matches.append(polar_session.start_time)
            sorted_polar_matches = sorted(polar_matches)
            first_polar_match = sorted_polar_matches.pop(0)
            final_matches.append((int_session.start_time, first_polar_match))
            unmatched_1.extend(polar_matches)  # all that is left is unmatched

        return FinalMatchingResult(
            matches=final_matches, unmatched_1=unmatched_1, unmatched_2=unmatched_2
        )

    polar: Dict = _get_start_time_to_session_mapping(polar_sessions)
    intensity: Dict = _get_start_time_to_session_mapping(intensity_sessions)
    potential_matching = _match_datetime_days(
        list(polar.keys()), list(intensity.keys())
    )
    final_matching = _match_session_type(
        potential_matching, polar_sessions, intensity_sessions
    )
    results = []
    for intensity_time, polar_time in final_matching.matches:
        base_session = polar[polar_time]
        sessions = [intensity[intensity_time]]
        results.append(add_sets_from_sessions(base_session, sessions))
    for time in final_matching.unmatched_1:
        results.append(polar[time])
    for time in final_matching.unmatched_2:
        results.append(intensity[time])
    return results

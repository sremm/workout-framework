import copy
from datetime import datetime
from typing import Dict, List, Tuple

from pydantic import BaseModel

from wof.domain.model import WorkoutSession


def add_sets_from_sessions(base_session: WorkoutSession, sessions_with_sets: List[WorkoutSession]) -> WorkoutSession:
    result = base_session
    for session in sessions_with_sets:
        result.add_sets(session.sets, origin=session.origin)
    return result


def are_on_same_day(time_1: datetime, time_2: datetime) -> bool:
    def _as_ymd(d: datetime) -> Tuple[int, int, int]:
        return (d.year, d.month, d.day)

    return _as_ymd(time_1) == _as_ymd(time_2)


class PotentialDatetimeMatches(BaseModel):
    intensity: datetime
    polar: List[datetime]


class PotentialMatchingResult(BaseModel):
    potential_matches: List[PotentialDatetimeMatches]
    unmatched_polar: List[datetime]
    unmatched_intensity: List[datetime]


class FinalMatchingResult(BaseModel):
    matches: List[Tuple[datetime, datetime]]
    unmatched_polar: List[datetime]
    unmatched_intensity: List[datetime]


def merge_polar_and_instensity_imports(
    polar_sessions: List[WorkoutSession], intensity_sessions: List[WorkoutSession]
) -> List[WorkoutSession]:
    def _get_start_time_to_session_mapping(
        sessions: List[WorkoutSession],
    ) -> Dict[datetime, WorkoutSession]:
        return {x.start_time: x for x in sessions}

    def _match_datetime_days(polar_times: List[datetime], intensity_times: List[datetime]) -> PotentialMatchingResult:
        """ Datetime based matching """
        matched_start_times = []
        unmatched_polar = []
        unmatched_intensity = []
        matched_polar = set()
        for intensity_time in intensity_times:
            current_matches = []
            # find all matches for time_2
            for polar_time in polar_times:
                if are_on_same_day(polar_time, intensity_time):
                    current_matches.append(polar_time)
                    matched_polar.add(polar_time)
            if current_matches != []:
                matched_start_times.append(PotentialDatetimeMatches(intensity=intensity_time, polar=current_matches))
            else:
                unmatched_intensity.append(intensity_time)
        # add all polar_times without match to result list
        for polar_time in polar_times:
            if polar_time not in matched_polar:
                unmatched_polar.append(polar_time)

        return PotentialMatchingResult(
            potential_matches=matched_start_times,
            unmatched_polar=unmatched_polar,
            unmatched_intensity=unmatched_intensity,
        )

    def _match_session_type(
        potential_results: PotentialMatchingResult,
        polar: Dict[datetime, WorkoutSession],
        intensity: Dict[datetime, WorkoutSession],
    ) -> FinalMatchingResult:
        final_matches = []
        unmatched_polar = copy.copy(potential_results.unmatched_polar)
        unmatched_intensity = copy.copy(potential_results.unmatched_intensity)
        for potential_matches in potential_results.potential_matches:
            int_session = intensity[potential_matches.intensity]
            polar_sessions = [polar[x] for x in potential_matches.polar]
            polar_matches = []
            for polar_session in polar_sessions:
                if polar_session.type == int_session.type:
                    polar_matches.append(polar_session.start_time)
                else:
                    unmatched_polar.append(polar_session.start_time)
            sorted_polar_matches = sorted(polar_matches)
            if sorted_polar_matches != []:
                first_polar_match = sorted_polar_matches.pop(0)
                final_matches.append((int_session.start_time, first_polar_match))
            else:
                unmatched_intensity.append(int_session.start_time)
            unmatched_polar.extend(sorted_polar_matches)  # all that is left is unmatched

        return FinalMatchingResult(
            matches=final_matches,
            unmatched_polar=unmatched_polar,
            unmatched_intensity=unmatched_intensity,
        )

    polar: Dict = _get_start_time_to_session_mapping(polar_sessions)
    intensity: Dict = _get_start_time_to_session_mapping(intensity_sessions)
    potential_matching = _match_datetime_days(list(polar.keys()), list(intensity.keys()))
    final_matching = _match_session_type(potential_matching, polar, intensity)
    results = []
    for intensity_time, polar_time in final_matching.matches:
        base_session = polar[polar_time]
        sessions = [intensity[intensity_time]]
        results.append(add_sets_from_sessions(base_session, sessions))
    for time in final_matching.unmatched_polar:
        results.append(polar[time])
    for time in final_matching.unmatched_intensity:
        results.append(intensity[time])
    results = sorted(results)
    return results

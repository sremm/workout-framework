from typing import DefaultDict, Dict, List

from wof.domain import commands
from wof.domain.analytics import WorkoutSessionsSummary, compute_workout_sessions_summary
from wof.domain.model import WorkoutSession
from wof.service_layer.unit_of_work import AbstractUnitOfWork


def workout_sessions(command: commands.GetSessions, uow: AbstractUnitOfWork) -> List[Dict]:
    def _get_query_args():
        result = DefaultDict(dict)
        if command.date_range.start is not None:
            result["start_time"]["$gt"] = command.date_range.start
        if command.date_range.end is not None:
            result["start_time"]["$lt"] = command.date_range.end
        return result

    with uow:
        results = uow.db_session.find(_get_query_args())
    return results


def workout_sessions_summary(
    command: commands.GetWorkoutSessionSummary, uow: AbstractUnitOfWork
) -> WorkoutSessionsSummary:
    sessions_dicts = workout_sessions(commands.GetSessions(date_range=command.date_range), uow)
    results = compute_workout_sessions_summary([WorkoutSession(**data) for data in sessions_dicts])
    return results

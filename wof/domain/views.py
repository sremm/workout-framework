from typing import DefaultDict, List, Dict

from wof.service_layer.unit_of_work import AbstractUnitOfWork
from wof.domain import commands


def workout_sessions(
    command: commands.GetSessions, uow: AbstractUnitOfWork
) -> List[Dict]:
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
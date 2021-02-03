from typing import DefaultDict, List, Dict, Optional

from wof.service_layer.unit_of_work import AbstractUnitOfWork
from wof.domain.commands import DateTimeRange


def workout_sessions(
    datetime_range: Optional[DateTimeRange], uow: AbstractUnitOfWork
) -> List[Dict]:
    def _get_query_args():
        result = DefaultDict(dict)
        if datetime_range is not None:
            result["start_time"]["$gt"] = datetime_range.start
            result["start_time"]["$lt"] = datetime_range.end
        return result

    with uow:
        results = uow.db_session.find(_get_query_args())
    return results
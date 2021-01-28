from typing import List

from wof.domain import events
from wof.domain.model import WorkoutSession
from wof.service_layer import unit_of_work


def import_sessions(
    event: events.ImportRequested, uow: unit_of_work.AbstractUnitOfWork
):
    def _convert(event: events.ImportRequested) -> events.SessionsToAdd:
        return events.SessionsToAdd(sessions=[])

    # convert to sessions
    sessions_to_add = _convert(event)
    add_workout_sessions(sessions_to_add, uow)


def add_workout_sessions(
    event: events.SessionsToAdd, uow: unit_of_work.AbstractUnitOfWork
) -> List:
    with uow:
        added_session_ids = uow.repo.add(event.sessions)
        uow.commit()
    return added_session_ids


class InvalidSessionId(Exception):
    pass


class DuplicateSessions(Exception):
    pass


def add_sets_to_workout_session(
    event: events.SetsCompleted, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        workout_sessions = uow.repo.get([event.session_id])
        if len(workout_sessions) == 1:
            uow.repo.update(event.session_id, event.sets)
            uow.commit()

        elif len(workout_sessions) == 0:
            raise InvalidSessionId(
                f"Found no workout sessions with {event.session_id=}"
            )
        else:
            raise DuplicateSessions(
                f"Found {len(workout_sessions)} sessions with {event.session_id=}, but should only get one"
            )

    return event.sets


def get_sessions(
    event: events.SessionsRequested, uow: unit_of_work.AbstractUnitOfWork
) -> List[WorkoutSession]:
    if event.date_range is None:
        return list_all_sessions(uow)
    else:
        # return sessions within event.date_range
        raise NotImplementedError


def list_all_sessions(uow: unit_of_work.AbstractUnitOfWork) -> List[WorkoutSession]:
    with uow:
        return uow.repo.list()

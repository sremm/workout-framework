from typing import List

from wof.domain.model import WorkoutSession, WorkoutSet
from wof.service_layer import messagebus
from wof.service_layer.unit_of_work import AbstractUnitOfWork


def add_workout_sessions(
    sessions: List[WorkoutSession], uow: AbstractUnitOfWork
) -> List:
    with uow:
        added_session_ids = uow.repo.add(sessions)
        uow.commit()
    return added_session_ids


class InvalidSessionId(Exception):
    pass


class DuplicateSessions(Exception):
    pass


def add_sets_to_workout_session(
    sets: List[WorkoutSet], session_id: str, uow: AbstractUnitOfWork
):
    with uow:
        workout_sessions = uow.repo.get([session_id])
        if len(workout_sessions) == 1:
            workout_session = uow.repo.update(session_id, sets)
            uow.commit()
            messagebus.handle_many(workout_session.events)

        elif len(workout_sessions) == 0:
            raise InvalidSessionId(f"Found no workout sessions with {session_id=}")
        else:
            raise DuplicateSessions(
                f"Found {len(workout_sessions)} sessions with {session_id=}, but should only get one"
            )

    return sets


def list_all_sessions(uow: AbstractUnitOfWork) -> List[WorkoutSession]:
    with uow:
        return uow.repo.list()

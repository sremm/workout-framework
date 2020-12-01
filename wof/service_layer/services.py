from typing import List
from wof.service_layer.unit_of_work import AbstractUnitOfWork

from wof.domain.model import WorkoutSession, WorkoutSet
from wof.adapters.repository import BaseRepository


def add_workout_sessions(
    sessions: List[WorkoutSession], uow: AbstractUnitOfWork
) -> None:
    with uow:
        uow.repo.add(sessions)
        uow.commit()


class InvalidSessionId(Exception):
    pass


def add_sets_to_workout_session(
    sets: List[WorkoutSet], session_id: str, uow: AbstractUnitOfWork
):
    with uow:
        workout_sessions = uow.repo.get([session_id])
        if len(workout_sessions) == 1:
            workout_session = workout_sessions[0]
            workout_session.add_sets(sets)
            uow.commit()
            return sets
        else:
            if len(workout_sessions) == 0:
                raise InvalidSessionId(f"Found no workout sessions with {session_id=}")
            else:
                raise Exception(
                    f"Found {len(workout_sessions)} sessions with {session_id=}, but should only get one"
                )


def list_all_sessions(uow: AbstractUnitOfWork) -> List[WorkoutSession]:
    with uow:
        return uow.repo.list()

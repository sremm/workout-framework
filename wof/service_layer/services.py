from typing import List
from wof.service_layer.unit_of_work import AbstractUnitOfWork

from wof.domain.model import WorkoutSession, WorkoutSet
from wof.adapters.repository import BaseRepository


def add_workout_sessions(
    sessions: List[WorkoutSession], repo: BaseRepository, db_session
) -> None:
    repo.add(sessions)
    db_session.commit()


class InvalidSessionId(Exception):
    pass


def add_sets_to_workout_session(
    sets: List[WorkoutSet], session_id: str, repo: BaseRepository, db_session
):
    workout_sessions = repo.get([session_id])
    if len(workout_sessions) == 1:
        workout_session = workout_sessions[0]
        workout_session.add_sets(sets)
        db_session.commit()
        return sets
    else:
        if len(workout_sessions) == 0:
            raise InvalidSessionId(f"Found no workout sessions with {session_id=}")
        else:
            raise Exception(
                f"Found {len(workout_sessions)} sessions with {session_id=}, but should only get one"
            )


def list_all_sessions(repo: BaseRepository) -> List[WorkoutSession]:
    return repo.list()


# def add_workout_sessions(sessions: List[WorkoutSession], uow: AbstractUnitOfWork):
#     with uow:
#         uow.repo.add(sessions)
#         uow.commit()
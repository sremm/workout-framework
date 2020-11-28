from typing import List
from wof.service_layer.unit_of_work import AbstractUnitOfWork

from wof.domain.model import WorkoutSession
from wof.adapters.base import BaseRepository


def add_workout_sessions(
    sessions: List[WorkoutSession], repo: BaseRepository, session
) -> None:
    repo.add(sessions)
    session.commit()


# def add_workout_sessions(sessions: List[WorkoutSession], uow: AbstractUnitOfWork):
#     with uow:
#         uow.repo.add(sessions)
#         uow.commit()
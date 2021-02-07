from typing import List

from wof.domain import commands, views
from wof.domain.model import WorkoutSession
from wof.service_layer import unit_of_work


def import_sessions(command: commands.ImportData, uow: unit_of_work.AbstractUnitOfWork):
    def _convert(command: commands.ImportData) -> commands.AddSessions:
        return commands.AddSessions(sessions=[])

    # convert to sessions
    sessions_to_add = _convert(command)
    add_workout_sessions(sessions_to_add, uow)


def add_workout_sessions(
    command: commands.AddSessions, uow: unit_of_work.AbstractUnitOfWork
) -> List:
    with uow:
        added_session_ids = uow.repo.add(command.sessions)
        uow.commit()
    return added_session_ids


class InvalidSessionId(Exception):
    pass


class DuplicateSessions(Exception):
    pass


def add_sets_to_workout_session(
    command: commands.AddSetsToSession, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        workout_sessions = uow.repo.get([command.session_id])
        if len(workout_sessions) == 1:
            uow.repo.update(command.session_id, command.sets)
            uow.commit()

        elif len(workout_sessions) == 0:
            raise InvalidSessionId(
                f"Found no workout sessions with {command.session_id=}"
            )
        else:
            raise DuplicateSessions(
                f"Found {len(workout_sessions)} sessions with {command.session_id=}, but should only get one"
            )

    return command.sets

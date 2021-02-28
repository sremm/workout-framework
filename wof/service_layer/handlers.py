from typing import List

from wof.domain import commands
from wof.import_workflows import data_merging, intensity_app, polar
from wof.service_layer import unit_of_work


def import_polar_data(command: commands.ImportSessionsFromPolarData, uow: unit_of_work.AbstractUnitOfWork):
    workout_sessions = polar.load_all_sessions_from_dicts(command.data)
    return add_workout_sessions(workout_sessions, uow)


def import_intensity_data(command: commands.ImportSessionsFromIntensityData, uow: unit_of_work.AbstractUnitOfWork):
    workout_sessions = intensity_app.import_from_file(command.data)
    return add_workout_sessions(workout_sessions, uow)


def merge_and_import_data(
    command: commands.ImportSessionsFromMergedPolarAndIntensityData, uow: unit_of_work.AbstractUnitOfWork
):
    polar_sessions = polar.load_all_sessions_from_dicts(command.polar_data)
    intensity_sessions = intensity_app.import_from_file(command.intensity_data)
    merged_sessions = data_merging.merge_polar_and_instensity_imports(polar_sessions, intensity_sessions)
    return add_workout_sessions(merged_sessions, uow)


def add_workout_sessions(command: commands.AddSessions, uow: unit_of_work.AbstractUnitOfWork) -> List:
    with uow:
        added_session_ids = uow.repo.add(command.sessions)
        uow.commit()
    return added_session_ids


class InvalidSessionId(Exception):
    pass


class DuplicateSessions(Exception):
    pass


def add_sets_to_workout_session(command: commands.AddSetsToSession, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        workout_sessions = uow.repo.get([command.session_id])
        if len(workout_sessions) == 1:
            uow.repo.update(command.session_id, command.sets)
            uow.commit()

        elif len(workout_sessions) == 0:
            raise InvalidSessionId(f"Found no workout sessions with {command.session_id=}")
        else:
            raise DuplicateSessions(
                f"Found {len(workout_sessions)} sessions with {command.session_id=}, but should only get one"
            )

    return command.sets

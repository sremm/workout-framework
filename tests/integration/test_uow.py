import os
from datetime import datetime
import threading
from typing import List

import pytest
from pymongo import MongoClient
from wof.adapters.mongo_db import MongoSettings, mongo_session_factory
from wof.domain import model
from wof.service_layer.unit_of_work import MongoUnitOfWork
import time
import traceback


def slow_update(
    session_factory, session_id, new_sets: List[model.WorkoutSet], exceptions: List
):

    try:
        uow = MongoUnitOfWork(session_factory)
        with uow:
            uow.repo.update(session_id, new_sets)
            time.sleep(0.2)
            uow.commit()
    except Exception as e:
        print(traceback.format_exc())
        exceptions.append(e)


class TestMongoUoW:
    def test_concurrent_updates_to_version_are_not_allowed(
        self, mongo_session_factory_instance
    ):
        """ Note that the result only has new_sets_2 but no exception is raised """
        uow = MongoUnitOfWork(mongo_session_factory_instance)
        with uow:
            workout_sessions = [model.WorkoutSession(sets=[model.WorkoutSet()])]
            added_session_ids = uow.repo.add(workout_sessions)
            uow.commit()
        new_sets_1, new_sets_2 = (
            [model.WorkoutSet(exercise="exercise_1")],
            [model.WorkoutSet(exercise="exercise_2")],
        )
        exceptions = []
        try_to_update_session_1 = lambda: slow_update(
            mongo_session_factory_instance, added_session_ids[0], new_sets_1, exceptions
        )
        try_to_update_session_2 = lambda: slow_update(
            mongo_session_factory_instance, added_session_ids[0], new_sets_2, exceptions
        )

        thread1 = threading.Thread(target=try_to_update_session_1)
        thread2 = threading.Thread(target=try_to_update_session_2)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        with uow:
            workout_session = uow.repo.get(added_session_ids)[0]

        assert workout_session.version == 2
        assert len(workout_session) == 2

    def test_uow_can_add_and_update_workout_sessions(
        self, mongo_session_factory_instance
    ):
        uow = MongoUnitOfWork(mongo_session_factory_instance)
        with uow:
            workout_sessions = [model.WorkoutSession(sets=[model.WorkoutSet()])]
            workout_sessions[0].start_time = datetime.strptime(
                str(workout_sessions[0].start_time)[:-3], "%Y-%m-%d %H:%M:%S.%f"
            )  # since mongodb truncates to milliseconds from microseconds
            added_session_ids = uow.repo.add(workout_sessions)
            uow.commit()
        fetched_sessions = uow.repo.get(added_session_ids)
        assert fetched_sessions == workout_sessions
        with uow:
            new_sets = [model.WorkoutSet()]
            uow.repo.update(added_session_ids[0], new_sets)
            uow.commit()
        fetched_session = uow.repo.get(added_session_ids)[0]
        assert len(fetched_session) == 2

    def test_rolls_back_uncommited_work_by_default(
        self, mongo_session_factory_instance
    ):
        uow = MongoUnitOfWork(mongo_session_factory_instance)
        with uow:
            workout_sessions = [
                model.WorkoutSession(id="abc123", sets=[model.WorkoutSet()])
            ]
            workout_sessions[0].start_time = datetime.strptime(
                str(workout_sessions[0].start_time)[:-3], "%Y-%m-%d %H:%M:%S.%f"
            )  # since mongodb truncates to milliseconds from microseconds
            uow.repo.add(workout_sessions)
        session_list = uow.repo.list()
        assert session_list == []

    def test_rolls_back_on_exception(self, mongo_session_factory_instance):
        uow = MongoUnitOfWork(mongo_session_factory_instance)

        class MyException(Exception):
            pass

        try:
            with uow:
                workout_sessions = [
                    model.WorkoutSession(id="abc123", sets=[model.WorkoutSet()])
                ]
                workout_sessions[0].start_time = datetime.strptime(
                    str(workout_sessions[0].start_time)[:-3], "%Y-%m-%d %H:%M:%S.%f"
                )  # since mongodb truncates to milliseconds from microseconds
                uow.repo.add(workout_sessions)
                raise MyException()
        except MyException:
            pass

        session_list = uow.repo.list()
        assert session_list == []

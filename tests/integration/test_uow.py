import os
from datetime import datetime
from typing import List

import pytest
from pymongo import MongoClient
from wof.adapters.csv import csv_session_factory
from wof.adapters.mongo_db import MongoSettings, mongo_session_factory
from wof.domain import model
from wof.service_layer.unit_of_work import CSVUnitOfWork, MongoUnitOfWork


@pytest.fixture
def mongo_session_factory_instance():
    # set env vars for MongoSettings
    evars = {
        "MONGO_DATABASE": "test_db",
        "MONGO_PORT": "27017",
        "MONGO_HOST": "localhost",
    }
    for key, val in evars.items():
        os.environ[key] = val
    yield mongo_session_factory(MongoSettings())
    # clear test database
    mongo_settings = MongoSettings()
    client = MongoClient(mongo_settings.mongo_host, mongo_settings.mongo_port)
    collection = client[mongo_settings.mongo_database][mongo_settings.main_collection]
    collection.drop()
    # remove environment variables
    for key, val in evars.items():
        os.environ.pop(key)


class TestMongoUoW:
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


@pytest.fixture
def csv_session_factory_instance(tmp_path):
    return csv_session_factory(tmp_path / "test_data.csv")


class TestCSVUoW:
    def test_uow_can_add_workout_sessions(self, csv_session_factory_instance):
        uow = CSVUnitOfWork(csv_session_factory_instance)
        with uow:
            workout_sessions = [
                model.WorkoutSession(id="abc123", sets=[model.WorkoutSet()])
            ]
            uow.repo.add(workout_sessions)
            uow.commit()
        fetched_session = uow.repo.get(["abc123"])
        assert fetched_session == workout_sessions

    def test_rolls_back_uncommited_work_by_default(self, csv_session_factory_instance):
        uow = CSVUnitOfWork(csv_session_factory_instance)
        with uow:
            workout_sessions = [
                model.WorkoutSession(id="abc123", sets=[model.WorkoutSet()])
            ]
            uow.repo.add(workout_sessions)
        session_list = uow.repo.list()
        assert session_list == []

    def test_rolls_back_on_exception(self, csv_session_factory_instance):
        class MyException(Exception):
            pass

        uow = CSVUnitOfWork(csv_session_factory_instance)
        try:
            with uow:
                workout_sessions = [
                    model.WorkoutSession(id="abc123", sets=[model.WorkoutSet()])
                ]
                uow.repo.add(workout_sessions)
                raise MyException()
        except MyException:
            pass

        session_list = uow.repo.list()
        assert session_list == []

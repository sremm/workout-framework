import os
import pytest
from pymongo import MongoClient
from wof.adapters.mongo_db import MongoSettings, mongo_session_factory


@pytest.fixture
def mongo_test_db():
    # set env vars for MongoSettings
    evars = {
        "MONGO_DATABASE": "test_db",
        "MONGO_PORT": "27017",
        "MONGO_HOST": "localhost",
    }
    for key, val in evars.items():
        os.environ[key] = val
    yield 1
    # clear test database
    mongo_settings = MongoSettings()
    client = MongoClient(mongo_settings.mongo_host, mongo_settings.mongo_port)
    collection = client[mongo_settings.mongo_database][mongo_settings.main_collection]
    collection.drop()
    # remove environment variables
    for key, val in evars.items():
        os.environ.pop(key)


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
import os
from typing import Dict

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from wof.adapters.mongo_db import MongoSettings
from wof.entrypoints.main import app


@pytest.fixture(scope="module")
def test_app():
    # set env vars for MongoSettings
    evars = {
        "MONGO_DATABASE": "test_db",
        "MONGO_PORT": "27017",
        "MONGO_HOST": "localhost",
    }
    for key, val in evars.items():
        os.environ[key] = val

    client = TestClient(app)
    yield client
    # clear test database
    mongo_settings = MongoSettings()
    client = MongoClient(mongo_settings.mongo_host, mongo_settings.mongo_port)
    collection = client[mongo_settings.mongo_database][mongo_settings.main_collection]
    collection.drop()
    # remove environment variables
    for key, val in evars.items():
        os.environ.pop(key)


def test_happy_path_add_session_add_sets_get_len(test_app):
    with test_app as client:  # this runs startup event
        set_data_1: Dict = {
            "exercise": "name",
            "reps": 1,
            "weights": 10.0,
            "set_number": 1,
            "unit": "kg",
        }
        response = client.put(
            "/workout_sessions",
            json=[set_data_1],
        )
        assert response.status_code == 200
        assert len(response.json()["workout_session_ids"]) == 1
        workout_session_id = response.json()["workout_session_ids"][0]

        set_data_2: Dict = {
            "exercise": "name",
            "reps": 1,
            "weights": 10.0,
            "set_number": 2,
            "unit": "kg",
        }
        response = client.post(
            f"/workout_sessions/{workout_session_id}",
            json=[set_data_2],
        )
        assert response.status_code == 200
        assert response.json() == {
            "msg": f"1 set(s) added to workout session {workout_session_id}"
        }

        response = client.get("/workout_sessions")
        results = response.json()
        del results[0]["start_time"]
        del results[0]["stop_time"]
        assert response.status_code == 200
        assert results == [
            {
                "sets": [set_data_1, set_data_2],
                "id": workout_session_id,
                "heart_rate": None,
                "version": 2,
                "events": [],
            }
        ]

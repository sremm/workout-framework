import os
import pytest
from fastapi.testclient import TestClient
from wof.entrypoints.main import app


@pytest.fixture(scope="module")
def test_app(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("csv_dataset") / "test_data.csv"

    os.environ["CSV_DATASET_PATH"] = str(tmp_path)
    client = TestClient(app)
    yield client
    os.environ.pop("CSV_DATASET_PATH")


def test_happy_path_add_session_add_sets_get_len(test_app):
    with test_app as client:  # this runs startup event
        # add an empty session
        workout_session_id = "123"
        response = client.post(f"/workout_sessions/{workout_session_id}")
        assert response.status_code == 200
        assert response.json() == {"workout_session_id": workout_session_id}

        response = client.get("/workout_sessions")
        assert response.status_code == 200
        assert response.json() == {"number_of_sessions": 1}

        response = client.put(f"/sets/{workout_session_id}")
        assert response.status_code == 200
        assert response.json() == {
            "msg": f"1 set(s) added to workout session {workout_session_id}"
        }

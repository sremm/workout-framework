import os
import pytest
from fastapi.testclient import TestClient
from wof.entrypoints.fast_api_app import app


@pytest.fixture(scope="module")
def test_app(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("csv_dataset")
    os.environ["CSV_DATASET_PATH"] = str(tmp_path)
    client = TestClient(app)
    yield client
    os.environ.pop("CSV_DATASET_PATH")


def test_get_sessions(test_app):
    with test_app as client:  # this runs startup event
        response = client.get("/sessions")
        assert response.status_code == 200
        assert response.json() == {"number_of_sessions": 0}

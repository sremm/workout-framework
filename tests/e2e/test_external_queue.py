from wof.domain.model import WorkoutSet


def test_add_sets_to_session():
    # build the command  for import
    command = {
        "type": "AddSetsToSession",
        "payload": {
            "session_id": "123",
            "sets": [WorkoutSet()],
        },
    }
    # send command to message queue

    # wait for response
    response_event = {}
    assert response_event == {
        "type": "DataImported",
        "payload": {"source": "IntensityApp", "num_sessions": 2},
    }

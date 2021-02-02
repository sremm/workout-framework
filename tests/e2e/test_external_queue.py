from typing import Dict


def _send_to_queue(command_data: Dict):
    pass


def test_create_session_with_sets():
    # build the commands
    set_data_1 = {
        "exercise": "name",
        "reps": 1,
        "weights": 10.0,
        "set_number": 1,
        "unit": "kg",
    }
    command_create = {
        "type": "CreateSession",
        "payload": {
            "sets": [set_data_1],
        },
    }
    # send commands to message queue
    _send_to_queue(command_create)

    # wait for response or I need a consumer to fetch events from queue
    response_event = {}
    assert response_event == {
        "type": "DataImported",
        "payload": {"source": "IntensityApp", "num_sessions": 2},
    }

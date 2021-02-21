import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
from wof.domain.model import SessionType, TimeSeries, WorkoutSession


class PolarFormatError(Exception):
    pass


def _confirm_export_format(data):
    if len(data["exercises"]) != 1:
        raise PolarFormatError(
            f"Expecting 1 entry in exercises, but got {len(data['exercises'])}"
        )


def _polar_date_conversion(date: str) -> datetime:
    return datetime.strptime(date + "000", "%Y-%m-%dT%H:%M:%S.%f")


def _convert_polar_samples(data: List[Dict], unit: str) -> Optional[TimeSeries]:
    values = []
    time = []
    for sample in data:
        if "value" not in sample.keys():
            values.append(np.nan)
        else:
            values.append(sample["value"])
        time.append(_polar_date_conversion(sample["dateTime"]))
    if np.all(np.isnan(values)):
        return None
    else:
        return TimeSeries(values=values, time=time, unit=unit)


def _convert_to_workout_session(data: Dict) -> WorkoutSession:
    _confirm_export_format(data)

    start_time = _polar_date_conversion(data["startTime"])

    heart_rate = _convert_polar_samples(
        data["exercises"][0]["samples"]["heartRate"], unit="bpm"
    )

    return WorkoutSession(
        type=SessionType(name=data["name"]),
        start_time=start_time,
        heart_rate=heart_rate,
        origin=["polar"],
    )


def load_all_sessions_in_folder(path: Path) -> List[WorkoutSession]:
    results = []
    for session_file_path in path.glob("training-session*.json"):
        with session_file_path.open("r") as f:
            data = json.load(f)
        results.append(_convert_to_workout_session(data))
    results.sort()
    return results


def load_all_sessions_from_dicts(data: List[Dict]) -> List[WorkoutSession]:
    results = []
    for session_data in data:
        results.append(_convert_to_workout_session(session_data))
    return results

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from wof.domain.model import TimeSeries, WorkoutSession


class PolarFormatError(Exception):
    pass


def confirm_export_format(data):
    if len(data["exercises"]) != 1:
        raise PolarFormatError(
            f"Expecting 1 entry in exercises, but got {len(data['exercises'])}"
        )


def polar_date_conversion(date: str) -> datetime:
    return datetime.strptime(date + "000", "%Y-%m-%dT%H:%M:%S.%f")


def load_all_sessions_in_folder(path: Path) -> List[WorkoutSession]:
    def _convert_polar_samples(data: List[Dict], unit: str) -> TimeSeries:
        values = []
        time = []
        for sample in data:
            values.append(sample["value"])
            time.append(polar_date_conversion(sample["dateTime"]))
        return TimeSeries(values=values, time=time, unit=unit)

    def _convert_to_workout_session(data: Dict) -> WorkoutSession:
        confirm_export_format(data)

        start_time = polar_date_conversion(data["startTime"])

        heart_rate = _convert_polar_samples(
            data["exercises"][0]["samples"]["heartRate"], unit="bpm"
        )

        return WorkoutSession(start_time=start_time, heart_rate=heart_rate)

    results = []
    for session_file_path in path.glob("training-session*.json"):
        with session_file_path.open("r") as f:
            data = json.load(f)
        results.append(_convert_to_workout_session(data))
    results.sort()
    return results

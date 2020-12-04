from pathlib import Path
from typing import Dict, List

from wof.domain.model import WorkoutSession

import json


def load_all_sessions_in_folder(path: Path) -> List[WorkoutSession]:
    def _convert_to_workout_session(data: Dict) -> WorkoutSession:
        return WorkoutSession()

    results = []
    for session_file_path in path.glob("training-session*.json"):
        with session_file_path.open("r") as f:
            data = json.load(f)
        results.append(_convert_to_workout_session(data))
    return results

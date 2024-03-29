""" Simple api with FastAPI to interact with workout-framework """

import json
import logging
from datetime import datetime
from typing import Any, Callable, List, Optional

import config
import orjson
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from wof.adapters.mongo_db import mongo_session_factory
from wof.bootstrap import bootstrap_handle
from wof.domain import commands, events
from wof.domain.analytics import WorkoutSessionsSummary
from wof.domain.model import DateTimeRange, WorkoutSession, WorkoutSet
from wof.service_layer import messagebus, unit_of_work

logging.basicConfig(format="%(asctime)s-%(levelname)s-%(message)s", level=logging.INFO)


class ORJSONResponse(JSONResponse):
    """ custom response to handle nans, cudos to https://github.com/tiangolo/fastapi/issues/459#issuecomment-536781105"""

    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(
            content,
            option=orjson.OPT_SERIALIZE_NUMPY,
        )


app = FastAPI(default_response_class=ORJSONResponse)


class Handle:
    def __init__(self) -> None:
        self._func = None

    def set_composed_handle(self, func: Callable):
        self._func = func

    def __call__(self, message: messagebus.Message) -> List:
        if self._func is not None:
            return self._func(message)
        else:
            logging.warning("Called handle without a composed function")
            return []


handle_composed = Handle()


@app.on_event("startup")
def startup():
    """ Initialise database """
    db_settings = config.MongoSettings()
    session_factory = mongo_session_factory(db_settings)
    uow = unit_of_work.MongoUnitOfWork(session_factory=session_factory)
    handle_composed.set_composed_handle(bootstrap_handle(uow=uow))


@app.put("/workout_sessions", tags=["workout_sessions"])
async def add_workout_session(workout_sets: List[WorkoutSet]):
    results = handle_composed(commands.AddSessions(sessions=[WorkoutSession(sets=workout_sets)]))
    session_ids = results.pop(0)
    return {"workout_session_ids": session_ids}


@app.post("/workout_sessions/{workout_session_id}", tags=["workout_sessions"])
async def add_sets_to_workout_session(workout_session_id: str, workout_sets: List[WorkoutSet]):
    results = handle_composed(
        commands.AddSetsToSession(sets=workout_sets, session_id=workout_session_id),
    )
    added_sets = results.pop(0)
    return {"msg": f"{len(added_sets)} set(s) added to workout session {workout_session_id}"}


@app.get("/workout_sessions", response_model=List[WorkoutSession], tags=["workout_sessions"])
async def in_datetime_range(
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
):
    results = handle_composed(commands.GetSessions(date_range=DateTimeRange(start=start, end=end)))
    fetched_sessions = results.pop(0)
    return fetched_sessions


@app.get("/analytics/workout_session_summary", response_model=WorkoutSessionsSummary, tags=["workout_sessions"])
def for_data_in_datetime_range(
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
):
    results = handle_composed(commands.GetWorkoutSessionSummary(date_range=DateTimeRange(start=start, end=end)))
    fetched_summary = results.pop(0)
    return fetched_summary


@app.post("/import/intensity", tags=["workout_sessions"])
def from_csv_file(file: UploadFile = File(...)):
    results = handle_composed(commands.ImportSessionsFromIntensityData(data=file.file._file))
    added_session_ids = results.pop(0)
    return {"number_of_sessions": len(added_session_ids)}


@app.post("/import/polar", tags=["workout_sessions"])
def from_json_files(files: List[UploadFile] = File(...)):
    results = handle_composed(commands.ImportSessionsFromPolarData(data=[json.load(x.file) for x in files]))
    added_session_ids = results.pop(0)
    return {"number_of_sessions": len(added_session_ids)}


@app.post("/import/polar_and_intensity_with_merge", tags=["workout_sessions"])
def from_json_and_csv_files(polar_files: List[UploadFile] = File(...), intensity_file: UploadFile = File(...)):
    results = handle_composed(
        commands.ImportSessionsFromMergedPolarAndIntensityData(
            polar_data=[json.load(x.file) for x in polar_files], intensity_data=intensity_file.file._file
        )
    )
    added_session_ids = results.pop(0)
    return {"number_of_sessions": len(added_session_ids)}


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--use-local-db",
        action="store_true",
        help="Use local db even when a remote db host is set",
    )
    args = parser.parse_args()
    if args.use_local_db:
        os.environ["MONGO_HOST"] = "localhost"

    uvicorn.run(app, host=config.api_settings.api_host, port=config.api_settings.api_port)

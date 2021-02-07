""" Simple api with FastAPI to interact with workout-framework """

import logging
from datetime import datetime
from typing import Callable, List, Optional

import config
import uvicorn
from fastapi import FastAPI, File, UploadFile
from wof.adapters.mongo_db import mongo_session_factory
from wof.domain import commands, events, views
from wof.domain.model import DateTimeRange, WorkoutSession, WorkoutSet
from wof.import_workflows import intensity_app
from wof.service_layer import messagebus, unit_of_work
from wof.bootstrap import bootstrap_handle

logging.basicConfig(format="%(asctime)s-%(levelname)s-%(message)s", level=logging.INFO)


app = FastAPI()


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


uow = {}
handle_composed = Handle()


@app.on_event("startup")
def startup():
    """ Initialise database """
    db_settings = config.MongoSettings()
    session_factory = mongo_session_factory(db_settings)
    uow["uow"] = unit_of_work.MongoUnitOfWork(session_factory=session_factory)
    handle_composed.set_composed_handle(bootstrap_handle(uow=uow["uow"]))


@app.put("/workout_sessions", tags=["workout_sessions"])
async def add_workout_session(workout_sets: List[WorkoutSet]):
    results = handle_composed(
        commands.AddSessions(sessions=[WorkoutSession(sets=workout_sets)])
    )
    session_ids = results.pop(0)
    return {"workout_session_ids": session_ids}


@app.post("/workout_sessions/{workout_session_id}", tags=["workout_sessions"])
async def add_sets_to_workout_session(
    workout_session_id: str, workout_sets: List[WorkoutSet]
):
    results = handle_composed(
        commands.AddSetsToSession(sets=workout_sets, session_id=workout_session_id),
    )
    added_sets = results.pop(0)
    return {
        "msg": f"{len(added_sets)} set(s) added to workout session {workout_session_id}"
    }


@app.get(
    "/workout_sessions", response_model=List[WorkoutSession], tags=["workout_sessions"]
)
async def in_datetime_range(
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
):
    results = views.workout_sessions(DateTimeRange(start=start, end=end), uow["uow"])
    return results


@app.post("/intensity_export", tags=["workout_sessions"])
def convert_and_add_sessions(file: UploadFile = File(...)):
    # TODO change to ImportRequested event/command
    workout_sessions = intensity_app.import_from_file(file.file)
    results = handle_composed(commands.AddSessions(sessions=workout_sessions))
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

    uvicorn.run(
        app, host=config.api_settings.api_host, port=config.api_settings.api_port
    )

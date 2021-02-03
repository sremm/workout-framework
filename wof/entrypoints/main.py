""" Simple api with FastAPI to interact with workout-framework """

import logging
from typing import List, Optional

from fastapi.param_functions import Body
from wof.adapters.mongo_db import mongo_session_factory

import config
import uvicorn
from fastapi import FastAPI, File, UploadFile
from wof.service_layer import unit_of_work
from wof.domain import events, commands, views
from wof.domain.model import WorkoutSession, WorkoutSet, DateTimeRange
from wof.import_logic import intensity_app
from wof.service_layer import messagebus

logging.basicConfig(format="%(asctime)s-%(levelname)s-%(message)s", level=logging.INFO)


app = FastAPI()

uow = {}


@app.on_event("startup")
def startup():
    """ Initialise database """
    db_settings = config.MongoSettings()
    session_factory = mongo_session_factory(db_settings)
    uow["uow"] = unit_of_work.MongoUnitOfWork(session_factory=session_factory)


@app.put("/workout_sessions", tags=["workout_sessions"])
async def add_workout_session(workout_sets: List[WorkoutSet]):
    results = messagebus.handle(
        commands.AddSessions(sessions=[WorkoutSession(sets=workout_sets)]), uow["uow"]
    )
    session_ids = results.pop(0)
    return {"workout_session_ids": session_ids}


@app.post("/workout_sessions/{workout_session_id}", tags=["workout_sessions"])
async def add_sets_to_workout_session(
    workout_session_id: str, workout_sets: List[WorkoutSet]
):
    results = messagebus.handle(
        commands.AddSetsToSession(sets=workout_sets, session_id=workout_session_id),
        uow["uow"],
    )
    added_sets = results.pop(0)
    return {
        "msg": f"{len(added_sets)} set(s) added to workout session {workout_session_id}"
    }


@app.get(
    "/workout_sessions", response_model=List[WorkoutSession], tags=["workout_sessions"]
)
async def workout_sessions_in_datetime_range(
    datetime_range: Optional[DateTimeRange] = Body(None),
):
    results = views.workout_sessions(datetime_range, uow["uow"])
    return results


@app.post("/intensity_export", tags=["workout_sessions"])
def import_intensity_app_data(file: UploadFile = File(...)):
    # TODO change to ImportRequested event/command
    workout_sessions = intensity_app.import_from_file(file.file)
    results = messagebus.handle(
        commands.AddSessions(sessions=workout_sessions), uow["uow"]
    )
    added_session_ids = results.pop(0)
    return {"number_of_sessions": len(added_session_ids)}


if __name__ == "__main__":
    uvicorn.run(
        app, host=config.api_settings.api_host, port=config.api_settings.api_port
    )

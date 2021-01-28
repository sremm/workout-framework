""" Simple api with FastAPI to interact with workout-framework """

import logging
from typing import List
from wof.adapters.mongo_db import mongo_session_factory

import config
import uvicorn
from fastapi import FastAPI, File, UploadFile
from wof.service_layer import unit_of_work
from wof.domain.model import WorkoutSession, WorkoutSet
from wof.import_logic import intensity_app
from wof.service_layer import handlers

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
    session_ids = handlers.add_workout_sessions(
        [WorkoutSession(sets=workout_sets)], uow["uow"]
    )
    return {"workout_session_ids": session_ids}


@app.post("/workout_sessions/{workout_session_id}", tags=["workout_sessions"])
async def add_sets_to_workout_session(
    workout_session_id: str, workout_sets: List[WorkoutSet]
):
    added_sets = handlers.add_sets_to_workout_session(
        workout_sets, workout_session_id, uow["uow"]
    )
    return {
        "msg": f"{len(added_sets)} set(s) added to workout session {workout_session_id}"
    }


@app.get(
    "/workout_sessions", response_model=List[WorkoutSession], tags=["workout_sessions"]
)
async def all_workout_sessions():
    all_sessions = handlers.list_all_sessions(uow["uow"])
    return all_sessions


@app.post("/intensity_export", tags=["workout_sessions"])
def allococate_in_batch(file: UploadFile = File(...)):
    workout_sessions = intensity_app.import_from_file(file.file)
    handlers.add_workout_sessions(workout_sessions, uow["uow"])
    return {"number_of_sessions": len(handlers.list_all_sessions(uow["uow"]))}


if __name__ == "__main__":
    uvicorn.run(
        app, host=config.api_settings.api_host, port=config.api_settings.api_port
    )

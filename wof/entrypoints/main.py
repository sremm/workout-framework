""" Simple api with FastAPI to interact with workout-framework """

import logging
from typing import List

import config
import uvicorn
from fastapi import FastAPI, File, UploadFile
from wof.adapters.repository import CSVRepository, CSVSession
from wof.domain.model import WorkoutSession, WorkoutSet
from wof.import_logic import intensity_app
from wof.service_layer import services

logging.basicConfig(format="%(asctime)s-%(levelname)s-%(message)s", level=logging.INFO)


app = FastAPI()

db = {}


@app.on_event("startup")
def startup():
    """ Initialise database """
    db_settings = config.DatabaseSettings()
    db["session"] = CSVSession(db_settings.csv_dataset_path)
    db["repo"] = CSVRepository(db["session"])


@app.put("/sets/{workout_session_id}", tags=["sets"])
async def add_sets_to_workout_session(
    workout_session_id: str, workout_sets: List[WorkoutSet]
):
    added_sets = services.add_sets_to_workout_session(
        workout_sets, workout_session_id, db["repo"], db["session"]
    )
    return {
        "msg": f"{len(added_sets)} set(s) added to workout session {workout_session_id}"
    }


@app.post("/workout_sessions/{workout_session_id}", tags=["workout_sessions"])
async def add_workout_sessions(workout_session_id: str):
    services.add_workout_sessions(
        [WorkoutSession(id=workout_session_id)], db["repo"], db["session"]
    )
    return {"workout_session_id": workout_session_id}


@app.get(
    "/workout_sessions", response_model=List[WorkoutSession], tags=["workout_sessions"]
)
async def all_workout_sessions():
    all_sessions = services.list_all_sessions(db["repo"])
    return all_sessions


@app.post("/intensity_export", tags=["workout_sessions"])
def allococate_in_batch(file: UploadFile = File(...)):
    workout_sessions = intensity_app.import_from_file(file.file)
    services.add_workout_sessions(workout_sessions, db["repo"], db["session"])
    return {"number_of_sessions": len(db["repo"].list())}


if __name__ == "__main__":
    uvicorn.run(
        app, host=config.api_settings.api_host, port=config.api_settings.api_port
    )

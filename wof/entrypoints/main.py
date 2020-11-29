""" Simple api with FastAPI to interact with workout-framework """

import logging
from wof.domain.model import WorkoutSession

import config
import uvicorn
from fastapi import FastAPI, File, UploadFile
from wof.adapters.repository import CSVRepository, CSVSession
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


@app.put("/workout_sessions/{workout_session_id}")
async def add_workout_sessions(workout_session_id: str):
    services.add_workout_sessions(
        [WorkoutSession(id=workout_session_id)], db["repo"], db["session"]
    )
    return {"workout_session_id": workout_session_id}


@app.get("/workout_sessions")
async def number():
    return {"number_of_sessions": len(db["repo"].list())}


@app.post("/intensity_export")
def allococate_in_batch(file: UploadFile = File(...)):
    workout_sessions = intensity_app.import_from_file(file.file)
    services.add_workout_sessions(workout_sessions, db["repo"], db["session"])
    return {"number_of_sessions": len(db["repo"].list())}


if __name__ == "__main__":
    uvicorn.run(
        app, host=config.api_settings.api_host, port=config.api_settings.api_port
    )

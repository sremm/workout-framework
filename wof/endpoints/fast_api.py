""" Simple api with FastAPI to interact with workout-framework """

import logging
from pathlib import Path
from typing import List

import uvicorn
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from wof.import_logic import intensity_app
from wof.repository.base import BaseRepository
from wof.repository.csv import CSVRepository, CSVSession
from wof.service_layer import services

logging.basicConfig(format="%(asctime)s-%(levelname)s-%(message)s", level=logging.INFO)


class ExampleInput(BaseModel):
    name: str
    price: float


app = FastAPI()

# initate database session
path_to_dataset = (
    Path(__file__).parent.parent.parent / "data" / "csv_dataset" / "data.csv"
)
db_session = CSVSession(path_to_dataset)


@app.post("/intensity_export")
async def allococate_in_batch(file: UploadFile = File(...)):
    sessions = intensity_app.import_from_file(file.file)
    repo: BaseRepository = CSVRepository(db_session)
    services.allocate_in_batch(sessions, repo, db_session)
    return {"number_of_sessions": len(repo.list())}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

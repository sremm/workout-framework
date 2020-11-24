""" Simple api with FastAPI to interact with workout-framework """

from pathlib import Path

from fastapi import FastAPI
from wof.repository.base import BaseRepository
from wof.repository.csv import CSVRepository
from pydantic import BaseModel


class ExampleInput(BaseModel):
    name: str
    price: float


app = FastAPI()

# initate repository
path_to_dataset = (
    Path(__file__).parent.parent.parent / "data" / "csv_dataset" / "data.csv"
)
repo: BaseRepository = CSVRepository(Path(path_to_dataset))


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/list_len")
def list_repository():
    return {"len": len(repo.list())}


@app.post("/sessions")
def allococate_in_batch(input: ExampleInput):
    return input

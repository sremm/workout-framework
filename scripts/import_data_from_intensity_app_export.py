from pathlib import Path

import click
from wof.import_logic import intensity_app
from wof.repository.base import BaseRepository
from wof.repository.csv import CSVRepository


@click.command()
@click.option("--path", type=str, help="Number of greetings.")
def add_to_repository(path: str):
    sessions = intensity_app.import_from_file(Path(path))
    repository: BaseRepository = CSVRepository()
    repository.add_sessions(sessions)


if __name__ == "__main__":
    add_to_repository()

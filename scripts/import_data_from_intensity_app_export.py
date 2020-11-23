""" Simple CLI to import data from intensity export file """
from pathlib import Path

import click
from wof.import_logic import intensity_app
from wof.repository.base import BaseRepository
from wof.repository.csv import CSVRepository


@click.command()
@click.option("--path-to-import", type=str, help="Path to file to import from")
@click.option(
    "--path-to-dataset",
    default="data/csv_dataset/data.csv",
    show_default=True,
    type=str,
    help="Path to file holding the csv dataset",
)
def add_to_repository(path_to_import: str, path_to_dataset: str):
    """ Simple CLI to import data from intensity export file """
    sessions = intensity_app.import_from_file(Path(path_to_import))
    repository: BaseRepository = CSVRepository(Path(path_to_dataset))
    repository.add(sessions)
    repository.commit()


if __name__ == "__main__":
    add_to_repository()

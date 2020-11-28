""" Simple CLI to import data from intensity export file """
from pathlib import Path

import click
from wof.import_logic import intensity_app
from wof.adapters.repository import BaseRepository
from wof.adapters.repository import CSVRepository, CSVSession
from wof.service_layer import services

import logging

logging.basicConfig(format="%(asctime)s-%(levelname)s-%(message)s", level=logging.INFO)


@click.command()
@click.option("--path-to-import", type=str, help="Path to file to import from")
@click.option(
    "--path-to-dataset",
    default="data/csv_dataset/data.csv",
    show_default=True,
    type=str,
    help="Path to file holding the csv dataset",
)
def allocate_command(path_to_import: str, path_to_dataset: str):
    """ Simple CLI to import data from intensity export file """
    sessions = intensity_app.import_from_file(Path(path_to_import))
    logging.info(f"Sessions loaded from file: {path_to_import}")
    logging.info(f"Found {len(sessions)} unique sessions")
    db_session = CSVSession(Path(path_to_dataset))
    repository: BaseRepository = CSVRepository(db_session)
    services.add_workout_sessions(sessions, repository, db_session)
    logging.info("Imported data added to repository")


if __name__ == "__main__":
    allocate_command()

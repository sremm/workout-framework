import os
from pathlib import Path


def get_api_host():
    return os.environ.get("API_HOST", "localhost")


def get_api_port():
    return 5005 if get_api_host() == "localhost" else 80


def get_api_url() -> str:
    return f"http://{get_api_host()}:{get_api_port()}"


def get_csv_database_path() -> Path:
    return (Path(__file__).parent / "data" / "csv_dataset" / "data.csv").resolve()

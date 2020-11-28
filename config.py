from pathlib import Path
from pydantic import BaseSettings


class ApiSettings(BaseSettings):
    api_host: str = "localhost"
    api_port: int = 5005


api_settings = ApiSettings()


def get_api_url() -> str:
    return f"http://{api_settings.api_host}:{api_settings.api_port}"


def get_csv_database_path() -> Path:
    return (Path(__file__).parent / "data" / "csv_dataset" / "data.csv").resolve()


class DatabaseSettings(BaseSettings):
    csv_dataset_path: Path = get_csv_database_path()

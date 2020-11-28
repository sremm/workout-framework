from pathlib import Path

BACKEND_IP = "localhost"
BACKEND_PORT = 8000


def get_csv_database_path():
    return (
        Path(__file__).parent/ "data" / "csv_dataset" / "data.csv"
    ).resolve()

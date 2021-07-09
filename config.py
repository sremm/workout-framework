from pydantic import BaseSettings


class MongoSettings(BaseSettings):
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_database: str = "test_db"
    main_collection: str = "workout_sessions"

    class Config:
        env_file = ".env"


class ApiSettings(BaseSettings):
    api_host: str = "localhost"
    api_port: int = 5005


api_settings = ApiSettings()


def get_api_url() -> str:
    return f"http://{api_settings.api_host}:{api_settings.api_port}"

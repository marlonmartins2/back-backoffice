import os

from dotenv import load_dotenv

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the application

        :param BaseSettings: Pydantic BaseSettings
    """

    load_dotenv()

    # General
    APP_NAME: str = os.getenv("APP_NAME")
    APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION")
    DEBUG: bool = bool(int(os.getenv("DEBUG", 0)))
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS").split(",")

    # Mongo
    MONGO_URL: str = os.getenv("MONGO_URL")
    MONGO_SSL: bool = bool(int(os.getenv("MONGO_SSL")))
    PATH_CERT: str = os.getenv("PATH_CERT")
    DATABASE_ENVIRONMENT: str = os.getenv("DATABASE_ENVIRONMENT")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    REFRESH_SECRET_KEY: str = os.getenv("REFRESH_SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

settings = Settings()

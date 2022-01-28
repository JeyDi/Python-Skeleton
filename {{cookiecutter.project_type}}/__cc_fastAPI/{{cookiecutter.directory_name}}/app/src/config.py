# This is direct configuration for the project
# Next step is converting to a pydantic config class

import os
import secrets
from typing import List, Any, Dict, Optional, Union, Tuple
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, PostgresDsn, validator
from pydantic.env_settings import SettingsSourceCallable


class Settings(BaseSettings):
    """
    Settings class for application settings and secrets management
    Official documentation on pydantic settings management:
    - https://pydantic-docs.helpmanual.io/usage/settings/
    """

    API_ENDPOINT_PORT: int = 8000
    APP_DOCKER_PORT: int = 8042
    API_ENDPOINT_HOST: str = "127.0.0.1"
    APP_SECRET_KEY: str = "DEVtest42!!"
    APP_API_TOKEN: str = "FASTapiToken42!"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "fastapi"

    # Application Path
    APP_PATH: str = os.path.abspath(".")

    # Path for optional app configurations
    CONFIG_PATH: str = os.path.join(APP_PATH, "app", "config")

    # if you want to test gunicorn the below environment variabile must be False
    DEBUG_MODE: str = "True"
    APP_VERBOSITY: str = "DEBUG"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # security aspects
    SECURITY_ALGORITHM: str = "HS256"
    SECURITY_SECRET_KEY: str = secrets.token_urlsafe(32)
    SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    DB_NAME: str = "fastapi"
    DB_USER: str = "root"
    DB_PASSWORD: str = "SUPERduper42"
    DB_PORT: str = "5442"
    DB_HOST: str = "localhost"
    # required to use the assemble_db_connection properties (you can use directly this prop for the db connection string)
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=values.get("DB_PORT"),
            path=f"/{values.get('DB_NAME') or ''}",
        )

    # Celery configuration
    CELERY_BROKER_URI: str = "redis://localhost:6379/0"
    CELERY_BACKEND_URI: str = "redis://localhost:6379/0"

    # email validation
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    # First default admin user details
    APP_USER_USERNAME: str = "pbg"
    APP_USER_EMAIL: str = "pythonbiellagroup@gmail.com"
    APP_USER_NAME: str = "PythonBiellaGroup"
    APP_USER_SURNAME: str = "PythonBiellaGroup"
    APP_USER_PASSWORD: str = "adminMEGA42!"
    APP_USER_TOKEN: str = "123PROVIssimo!"
    # APP_USER_BIRTH_DATE: date = datetime.strptime("2021-10-11"), "%Y-%m-%d").date()
    APP_USER_ISADMIN: bool = bool("True")

    class Config:
        case_sensitive = True

        # if you want to read the .env files
        env_file = ".env"
        env_file_encoding = "utf-8"

        # if you want to set the priority order of the settings env reading
        # top is with the high priority
        @classmethod
        def customise_sources(
            cls,
            env_settings: SettingsSourceCallable,
            init_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return env_settings, init_settings, file_secret_settings


# define the settings
settings = Settings()

import os
from dotenv import load_dotenv

from pydantic import AnyHttpUrl, BaseSettings, validator

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api_v1"
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    ALGORITHM: str = os.getenv("ALGORITHM")
    CLEARBIT_API_KEY: str = os.getenv("CLEARBIT_API_KEY")
    EMAIL_HUNTER_API_KEY: str = os.getenv("EMAIL_HUNTER_API_KEY")

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = [
        "http://localhost",
        "http://127.0.0.1",
    ]
    BACKEND_HOST_ORIGINS: list[AnyHttpUrl] = [
        "http://localhost",
        "http://127.0.0.1",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    DATABASE_DSN: str = "postgresql+psycopg2://postgres:password@social-network-fastapi-db:5432/social-network-fastapi"
    CLEARBIT_URL: str = "https://person.clearbit.com/v2/people/find"
    EMAIL_HUNTER_URL: str = "https://api.hunter.io/v2/email-verifier"

    class Config:
        case_sensitive = True


settings = Settings()

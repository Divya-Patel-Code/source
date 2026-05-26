from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(".env")

class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
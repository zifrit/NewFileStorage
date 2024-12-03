from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "media"


class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_ASYNC(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class Settings(BaseSettings):
    PROJECT_TITLE: str
    PROJECT_HOST: str = "localhost"
    PROJECT_PORT: int = 8000
    HOST_URL: str = f"http://{PROJECT_HOST}:{PROJECT_PORT}"
    ALLOWED_ORIGINS: str = (
        "http://0.0.0.0, http://127.0.0.1, http://localhost, http://app"
    )
    MAX_SIZE_FILE: int = 1024 * 1024  # 1 mb
    db_settings: DBSettings = DBSettings()

settings = Settings()

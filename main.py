import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from src.utils.logger import LOGGING
from src.core.settings import settings
from src.api.v1 import files


@asynccontextmanager
async def lifespan(app: FastAPI):
    media_dir = Path("./media")
    media_dir.mkdir(exist_ok=True)
    yield


app = FastAPI(
    title=settings.PROJECT_TITLE,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.include_router(files.router, prefix="/api/files", tags=["files"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )

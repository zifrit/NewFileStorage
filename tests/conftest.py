import asyncio
import pytest
import pytest_asyncio

from src.core.settings import settings
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
        base_url=settings.HOST_URL, transport=ASGITransport(app=app)
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def make_get_request(async_client):
    async def inner(
        path: str,
        query_params: dict | None = {},
    ):
        response = await async_client.get(
            path,
            params=query_params,
        )
        return response

    return inner


@pytest_asyncio.fixture
async def make_post_request(async_client):
    async def inner(
        path: str,
        json: dict | None = None,
        files: dict | None = None,
        query_params: dict = {},
    ):
        response = await async_client.post(
            path,
            json=json,
            files=files,
            params=query_params,
        )
        return response

    return inner

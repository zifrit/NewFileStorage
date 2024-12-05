import os
import http
import uuid

import pytest
from tests.settings import TEST_DATA_DIR


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "path": "/api/files/upload",
                "data": {
                    "file_name": "common_text.txt",
                },
            },
            {
                "response": {
                    "file_size": 110100,
                    "file_format": "text/plain",
                    "file_old_name": "common_text.txt",
                    "file_extension": ".txt",
                },
                "status": http.HTTPStatus.OK,
            },
        )
    ],
)
@pytest.mark.asyncio
async def tests_upload_files(
    make_post_request,
    query: dict,
    expected_answer: dict,
):
    test_file = TEST_DATA_DIR / query["data"]["file_name"]
    with test_file.open("rb") as f:
        response = await make_post_request(
            files={"file": (query["data"]["file_name"], f, "text/plain")},
            path=query["path"],
        )
        assert response.json()["file_size"] == expected_answer["response"]["file_size"]
        assert (
            response.json()["file_format"] == expected_answer["response"]["file_format"]
        )
        assert (
            response.json()["file_old_name"]
            == expected_answer["response"]["file_old_name"]
        )
        assert (
            response.json()["file_extension"]
            == expected_answer["response"]["file_extension"]
        )
        assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "path": "/api/files/upload",
                "data": {
                    "file_name": "large_text.txt",
                },
            },
            {
                "response": {"detail": "File is too large."},
                "status": http.HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
            },
        )
    ],
)
@pytest.mark.asyncio
async def tests_upload_file_with_large_false(
    make_post_request,
    query: dict,
    expected_answer: dict,
):
    test_file = TEST_DATA_DIR / query["data"]["file_name"]
    with test_file.open("rb") as f:
        response = await make_post_request(
            files={"file": (query["data"]["file_name"], f, "text/plain")},
            path=query["path"],
        )
        assert response.json() == expected_answer["response"]
        assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "path": "/api/files/upload",
                "data": {
                    "file_name": "large_text.txt",
                },
            },
            {
                "response": {
                    "file_size": 1101000,
                    "file_format": "text/plain",
                    "file_old_name": "large_text.txt",
                    "file_extension": ".txt",
                },
                "status": http.HTTPStatus.OK,
            },
        )
    ],
)
@pytest.mark.asyncio
async def tests_upload_file_with_large_true(
    make_post_request,
    query: dict,
    expected_answer: dict,
):
    test_file = TEST_DATA_DIR / query["data"]["file_name"]
    with test_file.open("rb") as f:
        response = await make_post_request(
            files={"file": (query["data"]["file_name"], f, "text/plain")},
            query_params={"large": True},
            path=query["path"],
        )
        assert response.json()["file_size"] == expected_answer["response"]["file_size"]
        assert (
            response.json()["file_format"] == expected_answer["response"]["file_format"]
        )
        assert (
            response.json()["file_old_name"]
            == expected_answer["response"]["file_old_name"]
        )
        assert (
            response.json()["file_extension"]
            == expected_answer["response"]["file_extension"]
        )
        assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "path": "/api/files/upload",
                "data": {
                    "file_name": "very_large_text.txt",
                },
            },
            {
                "response": {"detail": "File is too large."},
                "status": http.HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
            },
        )
    ],
)
@pytest.mark.asyncio
async def tests_upload_very_large_file_with_large_true(
    make_post_request,
    query: dict,
    expected_answer: dict,
):
    test_file = TEST_DATA_DIR / query["data"]["file_name"]
    with test_file.open("rb") as f:
        response = await make_post_request(
            files={"file": (query["data"]["file_name"], f, "text/plain")},
            query_params={"large": True},
            path=query["path"],
        )
        assert response.json() == expected_answer["response"]
        assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "path": {
                    "post": "/api/files/upload",
                    "get": "/api/files/",
                },
                "data": {
                    "file_name": "common_text.txt",
                },
            },
            {
                "response": {
                    "post": {
                        "file_size": 110100,
                        "file_format": "text/plain",
                        "file_old_name": "common_text.txt",
                        "file_extension": ".txt",
                    },
                },
                "status": {"post": http.HTTPStatus.OK, "get": http.HTTPStatus.OK},
            },
        )
    ],
)
@pytest.mark.asyncio
async def tests_get_invalid_files(
    make_post_request,
    make_get_request,
    query: dict,
    expected_answer: dict,
):
    test_file = TEST_DATA_DIR / query["data"]["file_name"]
    with test_file.open("rb") as f:
        post_response = await make_post_request(
            files={"file": (query["data"]["file_name"], f, "text/plain")},
            path=query["path"]["post"],
        )
        data = post_response.json()
        assert data["file_size"] == expected_answer["response"]["post"]["file_size"]
        assert data["file_format"] == expected_answer["response"]["post"]["file_format"]
        assert (
            data["file_old_name"]
            == expected_answer["response"]["post"]["file_old_name"]
        )
        assert (
            data["file_extension"]
            == expected_answer["response"]["post"]["file_extension"]
        )
        assert post_response.status_code == expected_answer["status"]["post"]
    get_response = await make_get_request(path=f"{query["path"]["get"]}{data["id"]}")
    assert data == get_response.json()
    assert get_response.status_code == expected_answer["status"]["get"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "path": "/api/files/",
                "data": {
                    "file_name": "common_text.txt",
                },
            },
            {
                "response": {"detail": "Not found"},
                "status": http.HTTPStatus.NOT_FOUND,
            },
        )
    ],
)
@pytest.mark.asyncio
async def tests_get_upload_files(
    make_get_request,
    query: dict,
    expected_answer: dict,
):

    response = await make_get_request(path=f"{query["path"]}{uuid.uuid4()}")
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]

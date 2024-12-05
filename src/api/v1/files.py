from typing import Annotated
from uuid import UUID

from fastapi import Depends, APIRouter, Query, HTTPException, Header
from fastapi import File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.db.session import db_session
from src.schemas.files import ShowFilesSchema
from src.services.crud.files import save_file_to_base, get_file, get_files
from src.utils.raising_http_excp import RaiseHttpException

router = APIRouter()


@router.get("/", response_model=list[ShowFilesSchema])
async def files_from_db(
    page_size: int = Query(
        ge=1, le=100, description="Количество элементов на странице", default=1
    ),
    page_number: int = Query(ge=1, description="Номер страницы", default=1),
    session: AsyncSession = Depends(db_session.get_session),
):
    """
    Получить список файлов из базы данных с пагинацией.

    - **page_size**: Количество элементов на странице (от 1 до 100).
    - **page_number**: Номер страницы для получения.

    **Ответы**:
    - **200 OK**: Список файлов.
    - **404 Not Found**: Если не найдено файлов (в случае пустой базы).
    """
    return await get_files(
        session=session, page_size=page_size, page_number=page_number
    )


@router.get("/{filed_id}", response_model=ShowFilesSchema)
async def file_from_db(
    filed_id: UUID,
    session: AsyncSession = Depends(db_session.get_session),
):
    """
    Получить файл по его ID из базы данных.

    - **filed_id**: Уникальный идентификатор файла.

    **Ответы**:
    - **200 OK**: Возвращает файл с указанным ID.
    - **404 Not Found**: Если файл с таким ID не найден.
    """
    file = await get_file(filed_id=filed_id, session=session)
    RaiseHttpException.check_is_exist(file)
    return file


def validate_chunk_size_if_large(large: bool, chunk_size: int | None = None):
    if large and chunk_size is None:
        raise HTTPException(
            status_code=400, detail="chunk_size is required when large is set to True."
        )
    return chunk_size


@router.post("/upload", response_model=ShowFilesSchema)
async def upload_file(
    file: UploadFile = File(...),
    large: bool = Query(default=False, description="Флаг для отправки больших файлов"),
    chunk_size: int | None = Query(
        ge=1,
        default=1024 * 1024,
        description="Размер пачки, по скольку которого будет приниматься данные",
    ),
    session: AsyncSession = Depends(db_session.get_session),
):
    """
    Загрузить файл на сервер и сохранить его в базе данных.

    - **file**: Файл, который загружается через POST запрос.

    **Ответы**:
    - **200 OK**: Возвращает информацию о загруженном файле.
    - **413 Payload Too Large**: Если размер файла превышает максимально допустимый размер.
    """
    if (file.size > settings.MAX_SIZE_FILE and not large) or (
        file.size > settings.STEAM_MAX_SIZE_FILE and large
    ):
        raise HTTPException(status_code=413, detail="File is too large.")
    return await save_file_to_base(
        file=file, session=session, large=large, chunk_size=chunk_size
    )

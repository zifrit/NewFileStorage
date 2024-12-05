from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.files import Files
from fastapi import UploadFile

from src.services.cloud_storage import upload_to_cloud
from src.services.upload_file import save_file_to_disk


async def save_file_to_base(
    file: UploadFile,
    session: AsyncSession,
    large: bool = False,
    chunk_size: int | None = None,
) -> Files:
    """
    Сохраняет файл на диск и записывает его метаданные в базу данных.

    :param file: Объект UploadFile, содержащий информацию и данные загружаемого файла.
    :param session: Асинхронная сессия SQLAlchemy для взаимодействия с базой данных.
    :param chunk_size: Размер блока для чтения и записи в байтах (по умолчанию 1MB).
    :param large: Условие для выбора способа загрузки файлом больших или малых
    :return: Объект Files, представляющий запись сохранённого файла в базе данных.
    """
    row_file_data = await save_file_to_disk(
        file=file, large=large, chunk_size=chunk_size
    )
    saved_file = Files(**row_file_data.model_dump())
    session.add(saved_file)
    await session.commit()
    await session.refresh(saved_file)

    # await upload_to_cloud(file_path=saved_file.file_path, uuid=saved_file.id)

    return saved_file


async def get_file(
    session: AsyncSession,
    filed_id: UUID,
) -> Files:
    """
    Получает объект файла из базы данных по его уникальному идентификатору (UUID).

    :param session: Асинхронная сессия SQLAlchemy для взаимодействия с базой данных.
    :param filed_id: UUID файла, который нужно получить.
    :return: Объект Files, представляющий файл из базы данных, или None, если файл не найден.
    """
    file = await session.scalar(select(Files).where(Files.id == filed_id))
    return file


async def get_files(
    page_size: int,
    page_number: int,
    session: AsyncSession,
) -> list[Files]:
    """
    Возвращает список файлов из базы данных с поддержкой пагинации.

    :param page_size: Количество файлов, возвращаемых на одной странице.
    :param page_number: Номер страницы для пагинации.
    :param session: Асинхронная сессия SQLAlchemy для взаимодействия с базой данных.
    :return: Список объектов Files, представляющих файлы из базы данных.
    """
    page_from = page_size * (page_number - 1)
    file = await session.scalars(select(Files).offset(page_from).limit(page_size))
    return list(file)

import logging
from pathlib import Path

from fastapi import UploadFile, HTTPException
from src.core.settings import UPLOAD_DIR, BASE_DIR
from datetime import datetime
import aiofiles
from src.schemas.files import CreateFilesSchema

logger = logging.getLogger(__name__)


def generate_filename(file: UploadFile) -> str:
    """
    Генерирует уникальное имя для файла, используя текущую дату и время.

    :param file: Объект UploadFile, содержащий информацию о загруженном файле.
    :return: Сформированное имя файла, содержащее метку времени и исходное имя файла.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    return f"uploaded-{timestamp}: {file.filename}"


def get_target_folder(file: UploadFile) -> Path:
    """
    Определяет путь к папке для сохранения файла, основываясь на его типе контента.
    Если папка не существует, она создаётся автоматически.

    :param file: Объект UploadFile, содержащий информацию о загруженном файле.
    :return: Путь к папке для сохранения файла.
    """
    content_type_folder = file.content_type.replace("/", "_")
    target_folder = UPLOAD_DIR / content_type_folder
    target_folder.mkdir(parents=True, exist_ok=True)
    return target_folder


async def save_to_disk(file: UploadFile, file_path: Path) -> None:
    """
    Сохраняет содержимое загруженного файла на диск по указанному пути.

    :param file: Объект UploadFile, содержащий загружаемый файл.
    :param file_path: Путь, по которому файл должен быть сохранён.
    :raises HTTPException: В случае ошибок чтения или записи.
    :return: None
    """
    try:
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
    except ValueError as e:
        logger.warning('When save streaming file "%s" error: %s', file_path, e)
        raise HTTPException(
            status_code=400, detail="Error reading file. Please try again."
        )
    except Exception as e:
        logger.warning('When save streaming file "%s" error: %s', file_path, e)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


async def save_stream_to_disk(
    file: UploadFile, file_path: Path, chunk_size: int
) -> None:
    """
    Сохраняет потоковый файл на диск по указанному пути.

    :param file: Объект UploadFile, содержащий загружаемый файл.
    :param file_path: Строковый путь, куда файл будет сохранён.
    :param chunk_size: Размер блока для чтения и записи в байтах (по умолчанию 1MB).
    :raises HTTPException: В случае ошибок чтения или записи.
    :return: None
    """
    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            while chunk := await file.read(chunk_size):
                await buffer.write(chunk)
    except ValueError as e:
        logger.warning('When save streaming file "%s" error: %s', file_path, e)
        raise HTTPException(
            status_code=400, detail="Error reading file. Please try again."
        )
    except Exception as e:
        logger.warning('When save streaming file "%s" error: %s', file_path, e)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


def create_file_metadata(
    file: UploadFile, file_path: Path, new_filename: str
) -> CreateFilesSchema:
    """
    Создаёт объект метаданных файла для сохранения в базу данных.

    :param file: Объект UploadFile, содержащий информацию о загруженном файле.
    :param file_path: Путь, по которому файл сохранён.
    :param new_filename: Сформированное новое имя файла.
    :return: Объект CreateFilesSchema, содержащий метаданные файла.
    """
    file_path = str(file_path.relative_to(BASE_DIR))
    file_extension = Path(file_path).suffix

    return CreateFilesSchema(
        file_path=file_path,
        file_size=file.size,
        file_old_name=file.filename,
        file_new_name=new_filename,
        file_extension=file_extension,
        file_format=file.content_type,
    )


async def save_file_to_disk(
    file: UploadFile,
    large: bool = False,
    chunk_size: int | None = None,
) -> CreateFilesSchema:
    """
    Полный процесс сохранения загруженного файла:
    - Генерация имени файла и пути.
    - Сохранение содержимого файла на диск.
    - Формирование метаданных файла.

    :param chunk_size: Размер блока для чтения и записи в байтах (по умолчанию 1MB).
    :param large: Условие для выбора способа загрузки файлом больших или малых
    :param file: Объект UploadFile, содержащий информацию и данные загружаемого файла.
    :return: Объект CreateFilesSchema с метаданными сохранённого файла.
    """
    target_folder = get_target_folder(file)
    new_filename = generate_filename(file)
    file_path = target_folder / new_filename
    if large and chunk_size:
        await save_stream_to_disk(file=file, file_path=file_path, chunk_size=chunk_size)
    else:
        await save_to_disk(file=file, file_path=file_path)

    return create_file_metadata(file, file_path, new_filename)

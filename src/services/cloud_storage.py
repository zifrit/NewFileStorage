from uuid import UUID

import aiohttp


async def upload_to_cloud(file_path: str, uuid: UUID) -> None:
    """
    Эмуляция отправки в облачное хранилище.
    :param file_path: Строковый путь, где файл находится.
    :param uuid: Уникальный идентификатор сохраненного в базе файла
    :return: None
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://fake-cloud-storage.com/upload",
            data={"uuid": str(uuid), "file": open(file_path, "rb")},
        ) as response:
            if response.status != 200:
                raise Exception("Failed to upload to cloud storage")

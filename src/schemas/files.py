from src.schemas.base import BaseSchema
from uuid import UUID


class FilesSchema(BaseSchema):
    file_size: int
    file_format: str
    file_old_name: str
    file_new_name: str
    file_extension: str
    file_path: str


class CreateFilesSchema(FilesSchema):
    pass


class ShowFilesSchema(FilesSchema):
    id: UUID

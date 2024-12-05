from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base


class Files(Base):
    """
    Таблица с метаданными файлов
    """

    __tablename__ = "files"

    file_size: Mapped[int] = mapped_column(comment="File size in bytes")
    file_path: Mapped[str] = mapped_column(
        String(255), comment="The relative path to the file"
    )
    file_format: Mapped[str] = mapped_column(String(255), comment="The file format")
    file_old_name: Mapped[str] = mapped_column(
        String(255), comment="The old name of the file"
    )
    file_new_name: Mapped[str] = mapped_column(
        String(255), comment="The new name of the file"
    )
    file_extension: Mapped[str] = mapped_column(
        String(255), comment="The file extension"
    )

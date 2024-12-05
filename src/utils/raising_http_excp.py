from fastapi import HTTPException
from starlette import status
from src.models.base import Base


class RaiseHttpException:

    @staticmethod
    def check_is_exist(item: Base | None) -> None:
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )

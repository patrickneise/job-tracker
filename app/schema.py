from typing import Any, Literal

from fastapi.responses import JSONResponse
from pydantic import BaseModel

ResultTypes = Literal["success", "fail", "error"]


class ResponseStructure(BaseModel):
    result: ResultTypes
    data: Any
    status_code: int


class CustomResponse(JSONResponse):
    def __init__(
        self, content: Any, status: ResultTypes, status_code: int = 200, *args, **kwargs
    ) -> None:
        content = ResponseStructure(
            data=content, status_code=status_code, status=status
        ).model_dump()
        super().__init__(content, status_code, *args, **kwargs)

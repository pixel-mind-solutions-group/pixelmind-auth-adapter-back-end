from pydantic import BaseModel, Field
from typing import Any, Optional


class CommonResponseDTO(BaseModel):
    data: Optional[Any] = Field(None, description="The data returned by the API")
    message: Optional[str] = Field(
        None, description="A message describing the result of the API call"
    )
    status: Optional[int] = Field(
        None, description="The status of the API call, e.g., 'success' or 'error'"
    )

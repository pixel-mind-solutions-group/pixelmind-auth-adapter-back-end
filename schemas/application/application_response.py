from pydantic import BaseModel, Field
from typing import Optional


class ApplicationResponseDTO(BaseModel):
    applicationId: Optional[int] = Field(None, description="The ID of the application")
    applicationName: Optional[str] = Field(
        None, description="The name of the application"
    )
    active: Optional[bool] = Field(
        None, description="Indicates whether the application is active"
    )
    uuid: Optional[str] = Field(None, description="The UUID of the application")

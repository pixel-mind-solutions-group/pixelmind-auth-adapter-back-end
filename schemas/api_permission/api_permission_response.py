from pydantic import BaseModel, Field
from typing import Optional


class ApiPermissionResponseDTO(BaseModel):
    apiPermissionId: Optional[int] = Field(None, description="The ID of the permission")
    apiPermissionName: Optional[str] = Field(
        None, description="The name of the permission"
    )
    description: Optional[str] = Field(
        None, description="The description of the permission"
    )
    active: Optional[bool] = Field(
        None, description="Indicates whether the permission is active"
    )
    createdAt: Optional[str] = Field(None, description="Created timestamp")
    createdBy: Optional[str] = Field(None, description="Created by user")


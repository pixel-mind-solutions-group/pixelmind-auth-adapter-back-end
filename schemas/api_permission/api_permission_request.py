from pydantic import BaseModel, Field
from typing import Optional


class ApiPermissionRequestDTO(BaseModel):
    apiPermissionId: Optional[int] = Field(
        None, description="The ID of the permission (pass to update)"
    )
    apiPermissionName: str = Field(..., description="The name of the permission")
    description: Optional[str] = Field(
        None, description="The description of the permission"
    )
    active: Optional[bool] = Field(
        default=True, description="Indicates whether the permission is active"
    )

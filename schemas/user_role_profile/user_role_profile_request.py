from pydantic import BaseModel, Field
from typing import Optional, List


class UserRoleProfileRequestDTO(BaseModel):
    realmId: int = Field(..., description="The ID of the realm")
    applicationId: int = Field(..., description="The ID of the application")
    userRoleId: int = Field(..., description="The ID of the user role")
    moduleIdList: List[Optional[int]] = Field(..., description="The list of module IDs (can be empty)")
    apiPermissionIdList: List[int] = Field(..., description="The list of API permission IDs")
    uiPermissionIdList: List[int] = Field(..., description="The list of UI permission IDs")

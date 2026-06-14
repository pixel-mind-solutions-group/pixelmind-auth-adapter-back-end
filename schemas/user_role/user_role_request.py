from pydantic import BaseModel, Field
from typing import Optional


class UserRoleRequestDTO(BaseModel):
    roleId: Optional[int] = Field(None, description="The ID of the role (pass to update)")
    realmId: int = Field(..., description="The ID of the realm")
    applicationId: int = Field(..., description="The ID of the application")
    roleName: str = Field(..., description="The name of the role")
    description: Optional[str] = Field(None, description="The description of the role")
    active: Optional[bool] = Field(default=True, description="Indicates whether the role is active")

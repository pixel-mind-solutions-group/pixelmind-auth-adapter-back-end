from pydantic import BaseModel, Field
from typing import Optional


class UserProfileRequestDTO(BaseModel):
    id: Optional[int] = Field(None, description="The ID of the user profile mapping (pass to update)")
    userId: int = Field(..., description="The ID of the user")
    realmId: int = Field(..., description="The ID of the realm")
    applicationId: int = Field(..., description="The ID of the application")
    userRoleId: int = Field(..., description="The ID of the user role")

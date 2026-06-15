from pydantic import BaseModel, Field
from typing import Optional, List


class UserRoleProfileModuleSyncDTO(BaseModel):
    moduleId: Optional[int] = Field(None, description="The ID of the module (None/null for application level)")
    apiPermissionIdList: List[int] = Field(default_factory=list, description="The list of API permission IDs for this module")
    uiPermissionIdList: List[int] = Field(default_factory=list, description="The list of UI permission IDs for this module")


class UserRoleProfileSyncRequestDTO(BaseModel):
    realmId: int = Field(..., description="The ID of the realm")
    applicationId: int = Field(..., description="The ID of the application")
    userRoleId: int = Field(..., description="The ID of the user role")
    modules: List[UserRoleProfileModuleSyncDTO] = Field(..., description="The list of module mappings to sync")

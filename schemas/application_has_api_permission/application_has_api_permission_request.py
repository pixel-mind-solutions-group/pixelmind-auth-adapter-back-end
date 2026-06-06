from pydantic import BaseModel, Field


class ApplicationHasApiPermissionRequestDTO(BaseModel):
    realmId: int = Field(..., description="The ID of the realm")
    applicationId: int = Field(..., description="The ID of the application")
    apiPermissionIdList: list[int] = Field(..., description="The list of API permission IDs")

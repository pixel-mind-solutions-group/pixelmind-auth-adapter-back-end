from pydantic import BaseModel, Field


class ApplicationHasUiPermissionRequestDTO(BaseModel):
    realmId: int = Field(..., description="The ID of the realm")
    applicationId: int = Field(..., description="The ID of the application")
    uiPermissionIdList: list[int] = Field(..., description="The list of UI permission IDs")

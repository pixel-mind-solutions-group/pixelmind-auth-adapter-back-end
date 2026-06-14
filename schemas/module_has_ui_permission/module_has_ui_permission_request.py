from pydantic import BaseModel, Field
from typing import Optional


class ModuleHasUiPermissionRequestDTO(BaseModel):
    moduleId: int = Field(..., description="The ID of the module")
    uiPermissionIdList: list[Optional[int]] = Field(..., description="The list of UI permission IDs")

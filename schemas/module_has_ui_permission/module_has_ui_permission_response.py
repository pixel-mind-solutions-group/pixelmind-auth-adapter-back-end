from pydantic import BaseModel, Field
from typing import Optional
from schemas.module.module_response import ModuleResponseDTO
from schemas.ui_permission.ui_permission_response import UiPermissionResponseDTO


class ModuleHasUiPermissionResponseDTO(BaseModel):
    id: Optional[int] = Field(None, description="The ID of the permission mapping")
    moduleId: Optional[int] = Field(None, description="The ID of the module")
    uiPermissionId: Optional[int] = Field(None, description="The ID of the UI permission")
    module: Optional[ModuleResponseDTO] = Field(None, description="The module details")
    uiPermission: Optional[UiPermissionResponseDTO] = Field(None, description="The UI permission details")

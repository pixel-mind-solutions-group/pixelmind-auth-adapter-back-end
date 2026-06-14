from pydantic import BaseModel, Field
from typing import Optional
from schemas.module.module_response import ModuleResponseDTO
from schemas.api_permission.api_permission_response import ApiPermissionResponseDTO


class ModuleHasApiPermissionResponseDTO(BaseModel):
    id: Optional[int] = Field(None, description="The ID of the permission mapping")
    moduleId: Optional[int] = Field(None, description="The ID of the module")
    apiPermissionId: Optional[int] = Field(None, description="The ID of the API permission")
    module: Optional[ModuleResponseDTO] = Field(None, description="The module details")
    apiPermission: Optional[ApiPermissionResponseDTO] = Field(None, description="The API permission details")

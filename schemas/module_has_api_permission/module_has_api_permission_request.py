from pydantic import BaseModel, Field
from typing import Optional


class ModuleHasApiPermissionRequestDTO(BaseModel):
    id: Optional[int] = Field(None, description="The ID of the permission mapping")
    moduleId: Optional[int] = Field(None, description="The ID of the module")
    apiPermissionIdList: Optional[list[Optional[int]]] = Field(
        None, description="The list of API permission IDs"
    )

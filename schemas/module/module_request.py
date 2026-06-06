from pydantic import BaseModel, Field
from typing import Optional


class ModuleRequestDTO(BaseModel):
    moduleId: Optional[int] = Field(
        None, description="The ID of the module (pass to update)"
    )
    realmId: int = Field(..., description="The ID of the realm")
    applicationId: int = Field(..., description="The ID of the application")
    moduleName: str = Field(..., description="The name of the module")
    active: Optional[bool] = Field(
        default=True, description="Indicates whether the module is active"
    )

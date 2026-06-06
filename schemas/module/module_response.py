from pydantic import BaseModel, Field
from typing import Optional
from schemas.realm.realm_response import RealmResponseDTO
from schemas.application.application_response import ApplicationResponseDTO


class ModuleResponseDTO(BaseModel):
    moduleId: Optional[int] = Field(None, description="The ID of the module")
    realmId: Optional[int] = Field(None, description="The ID of the realm")
    applicationId: Optional[int] = Field(None, description="The ID of the application")
    moduleName: Optional[str] = Field(None, description="The name of the module")
    active: Optional[bool] = Field(
        None, description="Indicates whether the module is active"
    )
    realm: Optional[RealmResponseDTO] = Field(
        None, description="The realm of the module"
    )
    application: Optional[ApplicationResponseDTO] = Field(
        None, description="The application of the module"
    )

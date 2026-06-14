from pydantic import BaseModel, Field
from typing import Optional
from schemas.realm.realm_response import RealmResponseDTO
from schemas.application.application_response import ApplicationResponseDTO
from schemas.user_role.user_role_response import UserRoleResponseDTO
from schemas.module.module_response import ModuleResponseDTO


class UserRoleHasModulesResponseDTO(BaseModel):
    id: Optional[int] = Field(None, description="The ID of the mapping")
    realmId: Optional[int] = Field(None, description="The ID of the realm")
    applicationId: Optional[int] = Field(None, description="The ID of the application")
    userRoleId: Optional[int] = Field(None, description="The ID of the user role")
    moduleId: Optional[int] = Field(None, description="The ID of the module (optional)")

    realm: Optional[RealmResponseDTO] = Field(None, description="The realm details")
    application: Optional[ApplicationResponseDTO] = Field(None, description="The application details")
    userRole: Optional[UserRoleResponseDTO] = Field(None, description="The user role details")
    module: Optional[ModuleResponseDTO] = Field(None, description="The module details")

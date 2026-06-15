from pydantic import BaseModel, Field
from typing import Optional
from schemas.realm.realm_response import RealmResponseDTO
from schemas.application.application_response import ApplicationResponseDTO
from schemas.user_role.user_role_response import UserRoleResponseDTO
from schemas.module.module_response import ModuleResponseDTO
from schemas.api_permission.api_permission_response import ApiPermissionResponseDTO


class UserRoleHasModulesHasApiPermissionResponseDTO(BaseModel):
    id: Optional[int] = Field(None, description="The ID of the mapping")
    realmId: Optional[int] = Field(None, description="The ID of the realm")
    applicationId: Optional[int] = Field(None, description="The ID of the application")
    userRoleId: Optional[int] = Field(None, description="The ID of the user role")
    moduleId: Optional[int] = Field(None, description="The ID of the module (optional)")
    apiPermissionId: Optional[int] = Field(None, description="The ID of the API permission")

    realm: Optional[RealmResponseDTO] = Field(None, description="The realm details")
    application: Optional[ApplicationResponseDTO] = Field(None, description="The application details")
    userRole: Optional[UserRoleResponseDTO] = Field(None, description="The user role details")
    module: Optional[ModuleResponseDTO] = Field(None, description="The module details")
    apiPermission: Optional[ApiPermissionResponseDTO] = Field(None, description="The API permission details")

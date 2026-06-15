from pydantic import BaseModel, Field
from typing import List
from schemas.user_role_profile.user_role_has_modules_has_api_permission_response import UserRoleHasModulesHasApiPermissionResponseDTO
from schemas.user_role_profile.user_role_has_modules_has_ui_permission_response import UserRoleHasModulesHasUiPermissionResponseDTO


class UserRoleProfileSearchResponseDTO(BaseModel):
    apiPermissions: List[UserRoleHasModulesHasApiPermissionResponseDTO] = Field(
        default_factory=list, description="The list of mapped API permissions"
    )
    uiPermissions: List[UserRoleHasModulesHasUiPermissionResponseDTO] = Field(
        default_factory=list, description="The list of mapped UI permissions"
    )

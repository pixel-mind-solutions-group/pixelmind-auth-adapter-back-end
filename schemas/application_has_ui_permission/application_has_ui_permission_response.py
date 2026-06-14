from pydantic import BaseModel, Field
from typing import Optional
from schemas.realm.realm_response import RealmResponseDTO
from schemas.application.application_response import ApplicationResponseDTO
from schemas.ui_permission.ui_permission_response import UiPermissionResponseDTO


class ApplicationHasUiPermissionResponseDTO(BaseModel):
    id: Optional[int] = Field(None, description="The ID of the permission mapping")
    realmId: Optional[int] = Field(None, description="The ID of the realm")
    applicationId: Optional[int] = Field(None, description="The ID of the application")
    uiPermissionId: Optional[int] = Field(
        None, description="The ID of the ui permission"
    )
    realm: Optional[RealmResponseDTO] = Field(None, description="The realm details")
    application: Optional[ApplicationResponseDTO] = Field(
        None, description="The application details"
    )
    uiPermission: Optional[UiPermissionResponseDTO] = Field(
        None, description="The ui permission details"
    )

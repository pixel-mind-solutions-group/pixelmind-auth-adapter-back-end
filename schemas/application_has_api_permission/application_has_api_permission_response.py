from pydantic import BaseModel, Field
from typing import Optional
from schemas.realm.realm_response import RealmResponseDTO
from schemas.application.application_response import ApplicationResponseDTO
from schemas.api_permission.api_permission_response import ApiPermissionResponseDTO


class ApplicationHasApiPermissionResponseDTO(BaseModel):
    id: Optional[int] = Field(None, description="The ID of the permission mapping")
    realmId: Optional[int] = Field(None, description="The ID of the realm")
    applicationId: Optional[int] = Field(None, description="The ID of the application")
    apiPermissionId: Optional[int] = Field(
        None, description="The ID of the api permission"
    )
    realm: Optional[RealmResponseDTO] = Field(None, description="The realm details")
    application: Optional[ApplicationResponseDTO] = Field(
        None, description="The application details"
    )
    apiPermission: Optional[ApiPermissionResponseDTO] = Field(
        None, description="The api permission details"
    )

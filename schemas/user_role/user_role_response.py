from pydantic import BaseModel, Field
from typing import Optional
from schemas.realm.realm_response import RealmResponseDTO
from schemas.application.application_response import ApplicationResponseDTO


class UserRoleResponseDTO(BaseModel):
    roleId: Optional[int] = Field(None, description="The ID of the role")
    realmId: Optional[int] = Field(None, description="The ID of the realm")
    applicationId: Optional[int] = Field(None, description="The ID of the application")
    roleName: Optional[str] = Field(None, description="The name of the role")
    description: Optional[str] = Field(None, description="The description of the role")
    active: Optional[bool] = Field(None, description="Indicates whether the role is active")

    realm: Optional[RealmResponseDTO] = Field(None, description="The realm details")
    application: Optional[ApplicationResponseDTO] = Field(None, description="The application details")

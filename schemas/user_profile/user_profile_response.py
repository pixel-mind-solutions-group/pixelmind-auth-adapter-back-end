from pydantic import BaseModel, Field
from typing import Optional
from schemas.user.user_response import UserResponseDTO
from schemas.realm.realm_response import RealmResponseDTO
from schemas.application.application_response import ApplicationResponseDTO
from schemas.user_role.user_role_response import UserRoleResponseDTO


class UserProfileResponseDTO(BaseModel):
    id: Optional[int] = Field(None, description="The ID of the user profile mapping")
    userId: Optional[int] = Field(None, description="The ID of the user")
    realmId: Optional[int] = Field(None, description="The ID of the realm")
    applicationId: Optional[int] = Field(None, description="The ID of the application")
    userRoleId: Optional[int] = Field(None, description="The ID of the user role")

    user: Optional[UserResponseDTO] = Field(None, description="The user details")
    realm: Optional[RealmResponseDTO] = Field(None, description="The realm details")
    application: Optional[ApplicationResponseDTO] = Field(None, description="The application details")
    userRole: Optional[UserRoleResponseDTO] = Field(None, description="The user role details")

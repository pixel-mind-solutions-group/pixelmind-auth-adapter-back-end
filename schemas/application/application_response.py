from pydantic import BaseModel, Field
from typing import Optional
from schemas.realm.realm_response import RealmResponseDTO


class ApplicationResponseDTO(BaseModel):
    id: Optional[int] = Field(None, description="The ID of the application")
    clientId: Optional[str] = Field(
        None, description="The client ID of the application"
    )
    uuid: Optional[str] = Field(None, description="The UUID of the application")
    active: Optional[bool] = Field(
        None, description="Indicates whether the application is active"
    )
    realm: Optional[RealmResponseDTO] = Field(
        None, description="The realm of the application"
    )

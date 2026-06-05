from pydantic import BaseModel, Field
from typing import Optional


class RealmResponseDTO(BaseModel):
    id: Optional[int] = Field(None, description="The ID of the realm")
    realm: Optional[str] = Field(None, description="The name of the realm")
    uuid: Optional[str] = Field(None, description="The UUID of the realm")
    active: Optional[bool] = Field(
        None, description="Indicates whether the realm is active"
    )

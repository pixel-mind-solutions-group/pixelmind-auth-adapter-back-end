from pydantic import BaseModel, Field
from typing import Optional, List


class UserDetailsResponseDTO(BaseModel):
    userId: Optional[int] = Field(None, description="The internal database ID of the user")
    username: str = Field(..., description="The username of the authenticated user")
    email: Optional[str] = Field(None, description="The email of the user")
    firstName: Optional[str] = Field(None, description="The first name of the user")
    lastName: Optional[str] = Field(None, description="The last name of the user")
    realm: Optional[str] = Field(None, description="The realm name")
    application: Optional[str] = Field(None, description="The application client ID")
    role: Optional[str] = Field(None, description="The assigned role name of the user")
    componentList: List[str] = Field(
        default_factory=list,
        description="List of UI Permissions / components assigned to this user role",
    )

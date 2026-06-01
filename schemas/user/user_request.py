from pydantic import BaseModel, Field
from typing import Any, Optional


from pydantic import BaseModel, Field
from typing import Optional


class UserRequestDTO(BaseModel):
    userId: Optional[int] = Field(None, description="The ID of the user")
    email: Optional[str] = Field(None, description="The email address of the user")
    firstName: Optional[str] = Field(None, description="The first name of the user")
    lastName: Optional[str] = Field(None, description="The last name of the user")
    username: Optional[str] = Field(None, description="The username of the user")
    password: Optional[str] = Field(None, description="The password of the user")

    active: Optional[bool] = Field(
        default=True, description="Indicates whether the user is active"
    )

    emailVerified: Optional[bool] = Field(
        default=False, description="Indicates whether the user's email is verified"
    )

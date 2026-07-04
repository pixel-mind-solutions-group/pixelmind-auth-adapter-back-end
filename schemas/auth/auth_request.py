from pydantic import BaseModel, Field


class TokenRequestDTO(BaseModel):
    username: str = Field(..., description="The username of the user")
    password: str = Field(..., description="The password of the user")
    application_uuid: str = Field(..., description="The unique identifier (UUID) of the application mapping")

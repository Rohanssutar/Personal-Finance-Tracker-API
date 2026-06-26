from enum import Enum
from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints


class UserRole(str, Enum):
    viewer = "viewer"
    analyst = "analyst"
    admin = "admin"


class UserCreate(BaseModel):
    username: Annotated[str, StringConstraints(min_length=3, max_length=50)]
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8)]
    role: UserRole

    model_config = ConfigDict(extra="forbid")


# Separate response schema — password is intentionally excluded
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(from_attributes=True)

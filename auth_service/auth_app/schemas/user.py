from pydantic import BaseModel, Field, ConfigDict

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=4, max_length=128)

class UserRead(BaseModel):
    id: int
    username: str
    is_admin: bool
    model_config = ConfigDict(from_attributes=True)
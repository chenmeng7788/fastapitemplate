from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    email: str
    full_name: str = None

class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes = True)


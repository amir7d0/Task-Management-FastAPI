from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Task(TaskBase):
    id: int
    completed: bool = False

    model_config = {
        "from_attributes": True,
    }


class UserBase(BaseModel):
    phone_number: str
    name: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserLoginOTP(BaseModel):
    phone_number: str


class UserVerifyOTP(BaseModel):
    phone_number: str
    code: str


class User(UserBase):
    id: int
    is_active: bool = True

    model_config = {
        "from_attributes": True,
    }


class LoginResponse(BaseModel):
    user: User
    access_token: str
    token_type: str = "bearer"

from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.user import UserResponse


class ClassCreate(BaseModel):
    name: str
    teacher_id: int


class ClassUpdate(BaseModel):
    name: Optional[str] = None
    teacher_id: Optional[int] = None


class ClassResponse(BaseModel):
    id: int
    name: str
    teacher_id: int
    teacher: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)

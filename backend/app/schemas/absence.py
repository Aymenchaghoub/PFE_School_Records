from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date
from app.schemas.user import UserResponse


class AbsenceCreate(BaseModel):
    student_id: int
    date: date
    reason: Optional[str] = None


class AbsenceUpdate(BaseModel):
    student_id: Optional[int] = None
    date: Optional[date] = None
    reason: Optional[str] = None


class AbsenceResponse(BaseModel):
    id: int
    student_id: int
    date: date
    reason: Optional[str] = None
    student: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)

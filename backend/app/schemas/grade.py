from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.user import UserResponse
from app.schemas.subject import SubjectResponse


class GradeCreate(BaseModel):
    student_id: int
    subject_id: int
    grade: float


class GradeUpdate(BaseModel):
    student_id: Optional[int] = None
    subject_id: Optional[int] = None
    grade: Optional[float] = None


class GradeResponse(BaseModel):
    id: int
    student_id: int
    subject_id: int
    grade: float
    created_at: datetime
    student: Optional[UserResponse] = None
    subject: Optional[SubjectResponse] = None

    model_config = ConfigDict(from_attributes=True)

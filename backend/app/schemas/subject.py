from pydantic import BaseModel, ConfigDict
from typing import Optional


class SubjectCreate(BaseModel):
    name: str
    class_id: int


class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    class_id: Optional[int] = None


class SubjectResponse(BaseModel):
    id: int
    name: str
    class_id: int

    model_config = ConfigDict(from_attributes=True)

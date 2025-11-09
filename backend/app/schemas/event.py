from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class EventCreate(BaseModel):
    title: str
    date: date
    description: Optional[str] = None


class EventUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[date] = None
    description: Optional[str] = None


class EventResponse(BaseModel):
    id: int
    title: str
    date: date
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

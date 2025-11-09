from sqlalchemy import Column, Integer, String, Date, Text
from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)

    # Relationships
    class_obj = relationship("Class", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")


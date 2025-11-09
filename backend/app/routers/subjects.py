from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.subject import Subject
from app.models.class_model import Class
from app.schemas.subject import SubjectResponse, SubjectCreate, SubjectUpdate
from app.core.security import get_current_user, require_role

router = APIRouter()


@router.get("/", response_model=List[SubjectResponse])
def get_subjects(
    class_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all subjects, optionally filtered by class."""
    query = db.query(Subject)
    if class_id:
        query = query.filter(Subject.class_id == class_id)
    return query.all()


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get subject by ID."""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


@router.post("/", response_model=SubjectResponse)
def create_subject(
    subject_data: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.TEACHER]))
):
    """Create a new subject."""
    class_obj = db.query(Class).filter(Class.id == subject_data.class_id).first()
    if not class_obj:
        raise HTTPException(status_code=400, detail="Class not found")
    
    new_subject = Subject(name=subject_data.name, class_id=subject_data.class_id)
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject


@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: int,
    subject_data: SubjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.TEACHER]))
):
    """Update subject."""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    if subject_data.name:
        subject.name = subject_data.name
    if subject_data.class_id:
        class_obj = db.query(Class).filter(Class.id == subject_data.class_id).first()
        if not class_obj:
            raise HTTPException(status_code=400, detail="Class not found")
        subject.class_id = subject_data.class_id
    
    db.commit()
    db.refresh(subject)
    return subject


@router.delete("/{subject_id}")
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.TEACHER]))
):
    """Delete subject."""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    db.delete(subject)
    db.commit()
    return {"message": "Subject deleted successfully"}


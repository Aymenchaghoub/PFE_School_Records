from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.absence import Absence
from app.models.class_model import Class
from app.models.subject import Subject
from app.models.grade import Grade
from app.schemas.absence import AbsenceResponse, AbsenceCreate, AbsenceUpdate
from app.core.security import get_current_user, require_role

router = APIRouter()


@router.get("/", response_model=List[AbsenceResponse])
def get_absences(
    student_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get absences, filtered by role permissions."""
    query = db.query(Absence)
    
    if current_user.role == UserRole.STUDENT:
        query = query.filter(Absence.student_id == current_user.id)
    elif current_user.role == UserRole.TEACHER:
        teacher_classes = db.query(Class).filter(Class.teacher_id == current_user.id).all()
        class_ids = [c.id for c in teacher_classes]
        teacher_subjects = db.query(Subject).filter(Subject.class_id.in_(class_ids)).all()
        subject_ids = [s.id for s in teacher_subjects]
        student_ids = db.query(Grade.student_id).filter(Grade.subject_id.in_(subject_ids)).distinct().all()
        student_ids = [s[0] for s in student_ids]
        query = query.filter(Absence.student_id.in_(student_ids))
    
    if student_id:
        query = query.filter(Absence.student_id == student_id)
    
    return query.order_by(Absence.date.desc()).all()


@router.get("/{absence_id}", response_model=AbsenceResponse)
def get_absence(
    absence_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get absence by ID."""
    absence = db.query(Absence).filter(Absence.id == absence_id).first()
    if not absence:
        raise HTTPException(status_code=404, detail="Absence not found")
    
    if current_user.role == UserRole.STUDENT and absence.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return absence


@router.post("/", response_model=AbsenceResponse)
def create_absence(
    absence_data: AbsenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.TEACHER]))
):
    """Create a new absence record."""
    student = db.query(User).filter(
        User.id == absence_data.student_id,
        User.role == UserRole.STUDENT
    ).first()
    if not student:
        raise HTTPException(status_code=400, detail="Student not found")
    
    new_absence = Absence(
        student_id=absence_data.student_id,
        date=absence_data.date,
        reason=absence_data.reason
    )
    db.add(new_absence)
    db.commit()
    db.refresh(new_absence)
    return new_absence


@router.put("/{absence_id}", response_model=AbsenceResponse)
def update_absence(
    absence_id: int,
    absence_data: AbsenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.TEACHER]))
):
    """Update absence record."""
    absence = db.query(Absence).filter(Absence.id == absence_id).first()
    if not absence:
        raise HTTPException(status_code=404, detail="Absence not found")
    
    if absence_data.student_id:
        absence.student_id = absence_data.student_id
    if absence_data.date:
        absence.date = absence_data.date
    if absence_data.reason is not None:
        absence.reason = absence_data.reason
    
    db.commit()
    db.refresh(absence)
    return absence


@router.delete("/{absence_id}")
def delete_absence(
    absence_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.TEACHER]))
):
    """Delete absence record."""
    absence = db.query(Absence).filter(Absence.id == absence_id).first()
    if not absence:
        raise HTTPException(status_code=404, detail="Absence not found")
    
    db.delete(absence)
    db.commit()
    return {"message": "Absence deleted successfully"}


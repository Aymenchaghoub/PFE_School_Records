from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.grade import Grade
from app.models.class_model import Class
from app.models.subject import Subject
from app.schemas.grade import GradeResponse, GradeCreate, GradeUpdate
from app.core.security import get_current_user, require_role

router = APIRouter()


@router.get("/", response_model=List[GradeResponse])
def get_grades(
    student_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get grades, filtered by role permissions."""
    query = db.query(Grade)
    
    if current_user.role == UserRole.STUDENT:
        query = query.filter(Grade.student_id == current_user.id)
    elif current_user.role == UserRole.TEACHER:
        teacher_classes = db.query(Class).filter(Class.teacher_id == current_user.id).all()
        class_ids = [c.id for c in teacher_classes]
        teacher_subjects = db.query(Subject).filter(Subject.class_id.in_(class_ids)).all()
        subject_ids = [s.id for s in teacher_subjects]
        query = query.filter(Grade.subject_id.in_(subject_ids))
    
    if student_id:
        query = query.filter(Grade.student_id == student_id)
    if subject_id:
        query = query.filter(Grade.subject_id == subject_id)
    
    return query.all()


@router.get("/{grade_id}", response_model=GradeResponse)
def get_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get grade by ID."""
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    
    if current_user.role == UserRole.STUDENT and grade.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return grade


@router.post("/", response_model=GradeResponse)
def create_grade(
    grade_data: GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.TEACHER]))
):
    """Create a new grade."""
    student = db.query(User).filter(
        User.id == grade_data.student_id,
        User.role == UserRole.STUDENT
    ).first()
    if not student:
        raise HTTPException(status_code=400, detail="Student not found")
    
    subject = db.query(Subject).filter(Subject.id == grade_data.subject_id).first()
    if not subject:
        raise HTTPException(status_code=400, detail="Subject not found")
    
    if grade_data.grade < 0 or grade_data.grade > 20:
        raise HTTPException(status_code=400, detail="Grade must be between 0 and 20")
    
    new_grade = Grade(
        student_id=grade_data.student_id,
        subject_id=grade_data.subject_id,
        grade=grade_data.grade
    )
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    return new_grade


@router.put("/{grade_id}", response_model=GradeResponse)
def update_grade(
    grade_id: int,
    grade_data: GradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.TEACHER]))
):
    """Update grade."""
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    
    if grade_data.grade is not None:
        if grade_data.grade < 0 or grade_data.grade > 20:
            raise HTTPException(status_code=400, detail="Grade must be between 0 and 20")
        grade.grade = grade_data.grade
    if grade_data.student_id:
        grade.student_id = grade_data.student_id
    if grade_data.subject_id:
        grade.subject_id = grade_data.subject_id
    
    db.commit()
    db.refresh(grade)
    return grade


@router.delete("/{grade_id}")
def delete_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.TEACHER]))
):
    """Delete grade."""
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    
    db.delete(grade)
    db.commit()
    return {"message": "Grade deleted successfully"}


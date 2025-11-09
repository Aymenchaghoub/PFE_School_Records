from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.class_model import Class
from app.schemas.class_model import ClassResponse, ClassCreate, ClassUpdate
from app.core.security import get_current_user, require_role

router = APIRouter()


@router.get("/", response_model=List[ClassResponse])
def get_classes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all classes."""
    query = db.query(Class)
    if current_user.role == UserRole.TEACHER:
        query = query.filter(Class.teacher_id == current_user.id)
    return query.all()


@router.get("/{class_id}", response_model=ClassResponse)
def get_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get class by ID."""
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_obj


@router.post("/", response_model=ClassResponse)
def create_class(
    class_data: ClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """Create a new class (Admin only)."""
    teacher = db.query(User).filter(
        User.id == class_data.teacher_id,
        User.role == UserRole.TEACHER
    ).first()
    if not teacher:
        raise HTTPException(status_code=400, detail="Teacher not found")
    
    new_class = Class(name=class_data.name, teacher_id=class_data.teacher_id)
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class


@router.put("/{class_id}", response_model=ClassResponse)
def update_class(
    class_id: int,
    class_data: ClassUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """Update class (Admin only)."""
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    
    if class_data.name:
        class_obj.name = class_data.name
    if class_data.teacher_id:
        teacher = db.query(User).filter(
            User.id == class_data.teacher_id,
            User.role == UserRole.TEACHER
        ).first()
        if not teacher:
            raise HTTPException(status_code=400, detail="Teacher not found")
        class_obj.teacher_id = class_data.teacher_id
    
    db.commit()
    db.refresh(class_obj)
    return class_obj


@router.delete("/{class_id}")
def delete_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """Delete class (Admin only)."""
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    
    db.delete(class_obj)
    db.commit()
    return {"message": "Class deleted successfully"}


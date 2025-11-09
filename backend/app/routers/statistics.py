from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.grade import Grade
from app.models.absence import Absence
from app.models.class_model import Class
from app.models.subject import Subject
from app.core.security import get_current_user

router = APIRouter()


@router.get("/dashboard")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard statistics based on user role."""
    stats = {}
    
    if current_user.role == UserRole.ADMIN:
        stats["total_users"] = db.query(func.count(User.id)).scalar()
        stats["total_students"] = db.query(func.count(User.id)).filter(User.role == UserRole.STUDENT).scalar()
        stats["total_teachers"] = db.query(func.count(User.id)).filter(User.role == UserRole.TEACHER).scalar()
        stats["total_classes"] = db.query(func.count(Class.id)).scalar()
        stats["total_subjects"] = db.query(func.count(Subject.id)).scalar()
        stats["total_grades"] = db.query(func.count(Grade.id)).scalar()
        stats["average_grade"] = db.query(func.avg(Grade.grade)).scalar() or 0
        stats["total_absences"] = db.query(func.count(Absence.id)).scalar()
        
    elif current_user.role == UserRole.TEACHER:
        teacher_classes = db.query(Class).filter(Class.teacher_id == current_user.id).all()
        class_ids = [c.id for c in teacher_classes]
        teacher_subjects = db.query(Subject).filter(Subject.class_id.in_(class_ids)).all()
        subject_ids = [s.id for s in teacher_subjects]
        
        stats["total_classes"] = len(teacher_classes)
        stats["total_subjects"] = len(teacher_subjects)
        stats["total_grades"] = db.query(func.count(Grade.id)).filter(Grade.subject_id.in_(subject_ids)).scalar()
        avg_grade = db.query(func.avg(Grade.grade)).filter(Grade.subject_id.in_(subject_ids)).scalar()
        stats["average_grade"] = float(avg_grade) if avg_grade else 0
        
        student_ids = db.query(Grade.student_id).filter(Grade.subject_id.in_(subject_ids)).distinct().all()
        student_ids = [s[0] for s in student_ids]
        stats["total_students"] = len(student_ids)
        stats["total_absences"] = db.query(func.count(Absence.id)).filter(Absence.student_id.in_(student_ids)).scalar()
        
    elif current_user.role == UserRole.STUDENT:
        stats["total_grades"] = db.query(func.count(Grade.id)).filter(Grade.student_id == current_user.id).scalar()
        avg_grade = db.query(func.avg(Grade.grade)).filter(Grade.student_id == current_user.id).scalar()
        stats["average_grade"] = float(avg_grade) if avg_grade else 0
        stats["total_absences"] = db.query(func.count(Absence.id)).filter(Absence.student_id == current_user.id).scalar()
        
        grades_by_subject = db.query(
            Subject.name,
            func.avg(Grade.grade).label('avg_grade'),
            func.count(Grade.id).label('count')
        ).join(Grade).filter(
            Grade.student_id == current_user.id
        ).group_by(Subject.id, Subject.name).all()
        
        stats["grades_by_subject"] = [
            {"subject": name, "average": float(avg), "count": count}
            for name, avg, count in grades_by_subject
        ]
    
    return stats


@router.get("/grades-distribution")
def get_grades_distribution(
    student_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get grades distribution by ranges."""
    query = db.query(Grade)
    
    if current_user.role == UserRole.STUDENT:
        query = query.filter(Grade.student_id == current_user.id)
    elif student_id:
        query = query.filter(Grade.student_id == student_id)
    
    if subject_id:
        query = query.filter(Grade.subject_id == subject_id)
    
    grades = query.all()
    
    distribution = {
        "0-5": len([g for g in grades if 0 <= g.grade < 5]),
        "5-10": len([g for g in grades if 5 <= g.grade < 10]),
        "10-15": len([g for g in grades if 10 <= g.grade < 15]),
        "15-20": len([g for g in grades if 15 <= g.grade <= 20])
    }
    
    return distribution


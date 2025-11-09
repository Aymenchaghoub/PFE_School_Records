from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User, UserRole
from app.core.security import get_current_user
from app.core.pdf_generator import generate_report_card

router = APIRouter()


@router.get("/report-card/{student_id}")
def get_report_card(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate and download PDF report card for a student."""
    if current_user.role == UserRole.STUDENT:
        if current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Not authorized to view this report")
    
    try:
        pdf_buffer = generate_report_card(student_id, db)
        return Response(
            content=pdf_buffer.read(),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=report_card_{student_id}.pdf"
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


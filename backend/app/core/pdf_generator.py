from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.models.grade import Grade
from app.models.absence import Absence
from io import BytesIO
from datetime import datetime


def generate_report_card(student_id: int, db: Session) -> BytesIO:
    """Generate PDF report card for a student."""
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        raise ValueError("Student not found")
    
    # Get all grades for the student
    grades = db.query(Grade).filter(Grade.student_id == student_id).all()
    
    # Get absences
    absences = db.query(Absence).filter(Absence.student_id == student_id).all()
    
    # Calculate statistics
    total_grades = len(grades)
    avg_grade = db.query(func.avg(Grade.grade)).filter(Grade.student_id == student_id).scalar() or 0
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#6A1B9A'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Title
    story.append(Paragraph("STUDENT REPORT CARD", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Student Info
    info_data = [
        ['Student Name:', student.name],
        ['Email:', student.email],
        ['Report Date:', datetime.now().strftime('%Y-%m-%d')]
    ]
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#6A1B9A')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Statistics
    stats_data = [
        ['Total Grades', 'Average Grade', 'Total Absences'],
        [str(total_grades), f"{avg_grade:.2f}", str(len(absences))]
    ]
    stats_table = Table(stats_data)
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6A1B9A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, 1), colors.lightgrey),
        ('FONTSIZE', (0, 1), (-1, 1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Grades Table
    if grades:
        grades_data = [['Subject', 'Grade', 'Date']]
        for grade in grades:
            grades_data.append([
                grade.subject.name if grade.subject else 'N/A',
                f"{grade.grade:.2f}",
                grade.created_at.strftime('%Y-%m-%d') if grade.created_at else 'N/A'
            ])
        
        grades_table = Table(grades_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        grades_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6A1B9A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(Paragraph("Grades", styles['Heading2']))
        story.append(grades_table)
        story.append(Spacer(1, 0.3*inch))
    
    # Absences Table
    if absences:
        absences_data = [['Date', 'Reason']]
        for absence in absences:
            absences_data.append([
                absence.date.strftime('%Y-%m-%d'),
                absence.reason or 'N/A'
            ])
        
        absences_table = Table(absences_data, colWidths=[3*inch, 3*inch])
        absences_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6A1B9A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(Paragraph("Absences", styles['Heading2']))
        story.append(absences_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer


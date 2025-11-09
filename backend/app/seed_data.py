"""
Seed script to create initial admin user and sample data.
Run this script after setting up the database:
    python -m app.seed_data
"""
from app.core.database import SessionLocal, init_db
from app.models.user import User, UserRole
from app.models.class_model import Class
from app.models.subject import Subject
from app.core.security import get_password_hash

# Initialize database
init_db()

db = SessionLocal()

try:
    # Create admin user
    admin_email = "admin@school.com"
    existing_admin = db.query(User).filter(User.email == admin_email).first()
    
    if not existing_admin:
        admin = User(
            name="Administrator",
            email=admin_email,
            password=get_password_hash("admin123"),
            role=UserRole.ADMIN
        )
        db.add(admin)
        db.commit()
        print(f"✅ Admin user created: {admin_email} / admin123")
    else:
        print(f"ℹ️  Admin user already exists: {admin_email}")
    
    # Create sample teacher
    teacher_email = "teacher@school.com"
    existing_teacher = db.query(User).filter(User.email == teacher_email).first()
    
    if not existing_teacher:
        teacher = User(
            name="John Teacher",
            email=teacher_email,
            password=get_password_hash("teacher123"),
            role=UserRole.TEACHER
        )
        db.add(teacher)
        db.commit()
        db.refresh(teacher)
        print(f"✅ Teacher user created: {teacher_email} / teacher123")
        
        # Create a class for the teacher
        new_class = Class(
            name="Class 10A",
            teacher_id=teacher.id
        )
        db.add(new_class)
        db.commit()
        db.refresh(new_class)
        print(f"✅ Class created: {new_class.name}")
        
        # Create subjects
        subjects = ["Mathematics", "Science", "English", "History"]
        for subject_name in subjects:
            subject = Subject(
                name=subject_name,
                class_id=new_class.id
            )
            db.add(subject)
        db.commit()
        print(f"✅ Created {len(subjects)} subjects")
        
    else:
        print(f"ℹ️  Teacher user already exists: {teacher_email}")
    
    # Create sample student
    student_email = "student@school.com"
    existing_student = db.query(User).filter(User.email == student_email).first()
    
    if not existing_student:
        student = User(
            name="Alice Student",
            email=student_email,
            password=get_password_hash("student123"),
            role=UserRole.STUDENT
        )
        db.add(student)
        db.commit()
        print(f"✅ Student user created: {student_email} / student123")
    else:
        print(f"ℹ️  Student user already exists: {student_email}")
    
    print("\n🎉 Seed data created successfully!")
    print("\n📝 Login Credentials:")
    print("   Admin: admin@school.com / admin123")
    print("   Teacher: teacher@school.com / teacher123")
    print("   Student: student@school.com / student123")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()


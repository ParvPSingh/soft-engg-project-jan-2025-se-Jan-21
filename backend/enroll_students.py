from application.models import User, Course, Enrollment
from application.database import db
from main import app

with app.app_context():
    # Fetch the only available course
    course = Course.query.first()  

    if not course:
        print("⚠️ No course found! Ensure a course exists in the database.")
    else:
        # Fetch all students (Users with the role "Student")
        students = User.query.filter(User.roles.any(name="Student")).all()

        if not students:
            print("⚠️ No students found! Ensure students exist in the database.")
        else:
            for student in students:
                # Check if student is already enrolled
                existing_enrollment = Enrollment.query.filter_by(course_id=course.course_id, student_id=student.user_id).first()
                
                if existing_enrollment:
                    print(f"⚠️ {student.name} is already enrolled in {course.name}. Skipping.")
                else:
                    # Create new enrollment record
                    new_enrollment = Enrollment(course_id=course.course_id, student_id=student.user_id)
                    db.session.add(new_enrollment)
                    print(f"✅ Enrolled {student.name} in {course.name}")

            db.session.commit()
            print("🎉 All students have been enrolled in the course!")

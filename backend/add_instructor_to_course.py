from application.models import InstructorAlloted, db

# Replace with actual instructor_id and course_id
instructor_id = 10
course_id = 1

# Check if the instructor is already assigned
existing_assignment = InstructorAlloted.query.filter_by(course_id=course_id, instructor_id=instructor_id).first()
if existing_assignment:
    print("⚠️ Instructor is already assigned to this course.")
else:
    # Create the assignment
    new_assignment = InstructorAlloted(course_id=course_id, instructor_id=instructor_id)
    db.session.add(new_assignment)
    db.session.commit()
    print("✅ Instructor assigned successfully!")

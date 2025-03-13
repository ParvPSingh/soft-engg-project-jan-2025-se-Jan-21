from application.models import User, Role
from application.database import db
from main import app  # Import Flask app to get database context

# Run inside Flask app context
with app.app_context():
    users = User.query.all()
    student_role = Role.query.filter_by(name="Student").first()

    if not student_role:
        print("⚠️ Role 'Student' not found. Please create it in the database.")
    else:
        for user in users:
            if not user.roles:  # If user has no role assigned
                user.roles.append(student_role)
                print(f"✅ Assigned 'Student' role to {user.name}")

        db.session.commit()
        print("🎉 Roles updated successfully!")

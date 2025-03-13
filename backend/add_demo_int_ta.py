from application.models import User, Role
from application.database import db
from main import app  # Import Flask app to use database context
from werkzeug.security import generate_password_hash

with app.app_context():
    # Define test users
    demo_users = [
        {"name": "InstructorDemo", "email": "instructor@test.com", "password": "123", "role": "Instructor"},
        {"name": "TADemo", "email": "ta@test.com", "password": "123", "role": "TA"}
    ]

    for user_data in demo_users:
        # Check if user already exists
        existing_user = User.query.filter_by(email=user_data["email"]).first()
        if existing_user:
            print(f"⚠️ User {user_data['email']} already exists. Skipping.")
            continue

        # Hash password
        hashed_password = generate_password_hash(user_data["password"], method="pbkdf2:sha256")

        # Create new user
        new_user = User(
            name=user_data["name"],
            email=user_data["email"],
            password=hashed_password,
            active=True,
            fs_uniquifier=user_data["email"]
        )

        # Assign role
        role = Role.query.filter_by(name=user_data["role"]).first()
        if role:
            new_user.roles.append(role)
        else:
            print(f"⚠️ Role {user_data['role']} not found! Make sure it's in the database.")

        db.session.add(new_user)

    # Commit changes
    db.session.commit()
    print("✅ Demo users added successfully!")

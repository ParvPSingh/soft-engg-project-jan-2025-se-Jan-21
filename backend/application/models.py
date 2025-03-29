from application.database import db
from flask_security import UserMixin, RoleMixin

class Role(db.Model, RoleMixin):
    __tablename__ = 'Role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

class User(db.Model, UserMixin):
    __tablename__="User"
    user_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    name=db.Column(db.String(25), unique=True)
    email=db.Column(db.String(25), unique=True, nullable=False)
    password=db.Column(db.String(25), unique=True, nullable=False)
    active=db.Column(db.Boolean)
    fs_uniquifier=db.Column(db.String(25), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='RolesUsers', backref=db.backref('users', lazy='dynamic'))

class RolesUsers(db.Model):
    __tablename__ = 'RolesUsers'
    ru_id = db.Column(db.Integer, primary_key=True)
    ru_user_id = db.Column('user_id', db.Integer, db.ForeignKey('User.user_id'))
    ru_role_id = db.Column('role_id', db.Integer, db.ForeignKey('Role.id'))

class Course(db.Model):
    __tablename__ = 'Course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    # relationships
    lectures = db.relationship('Lecture', backref='course', cascade="all, delete-orphan", lazy=True)
    assignments = db.relationship('Assignment', backref='course', cascade="all, delete-orphan", lazy=True)
    enrollments = db.relationship('Enrollment', backref='course', cascade="all, delete-orphan", lazy=True)
    feedbacks = db.relationship('Feedback', backref='course', cascade="all, delete-orphan", lazy=True)
    instructor_alloted = db.relationship('InstructorAlloted', backref='course', cascade="all, delete-orphan", lazy=True)

class Enrollment(db.Model):
    __tablename__ = 'Enrollment'
    enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    # relationships
    student = db.relationship('User', backref=db.backref('enrollments', lazy=True))

class InstructorAlloted(db.Model):
    __tablename__ = 'Instructor_alloted'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    # relationships
    instructor = db.relationship('User', backref=db.backref('courses_instructing', lazy=True))

class Lecture(db.Model):
    __tablename__ = 'Lecture'
    lecture_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    video_link = db.Column(db.String(255), nullable=False)
    lecture_no = db.Column(db.Integer, nullable=False)
    week_no = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

class Assignment(db.Model):
    __tablename__ = 'Assignment'
    assignment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'), nullable=False)
    assignment_no = db.Column(db.Integer, nullable=False)
    week_no = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    # relationships
    qas = db.relationship('QA', backref='assignment', cascade="all, delete-orphan", lazy=True)

class QA(db.Model):
    __tablename__ = 'QA'
    q_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    qa_assignment_id = db.Column(db.Integer, db.ForeignKey('Assignment.assignment_id'), nullable=False)
    options = db.Column(db.String(500), nullable=True)
    answer = db.Column(db.String(255), nullable=False)

class ProgQA(db.Model):
    __tablename__ = 'ProgQA'
    prog_q_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    prog_qa_assignment_id = db.Column(db.Integer, db.ForeignKey('Assignment.assignment_id'), nullable=False)
    prog_options = db.Column(db.String(500), nullable=True)
    prog_answer = db.Column(db.String(255), nullable=False)
    # relationships
    prog_assignment = db.relationship('Assignment', backref=db.backref('prog_qas', lazy=True))

class Scores(db.Model):
    __tablename__ = 'Scores'
    score_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score_user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    week_no = db.Column(db.Integer, nullable=True, default=0)
    score = db.Column(db.Integer, nullable=True, default=0)
    # relationships
    student = db.relationship('User', backref=db.backref('scores', lazy=True))

class Queries(db.Model):
    __tablename__ = 'Queries'
    query_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    query_student_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    # relationships
    student = db.relationship('User', backref=db.backref('queries', lazy=True))

class Feedback(db.Model):
    __tablename__ = 'Feedback'
    feed_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    feed_course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'), nullable=False)
    feed_user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    feed_rating = db.Column(db.Integer, nullable=False)
    feed_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    # relationships
    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))

class KnowledgeBase(db.Model):
    __tablename__ = 'KnowledgeBase'
    kb_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    kb_name = db.Column(db.String(255), nullable=False)
    kb_type = db.Column(db.String(50), nullable=False)
    kb_location = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())


    
class SupplementaryContent(db.Model):
    __tablename__ = 'SupplementaryContent'
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'), nullable=False)
    week_no = db.Column(db.Integer, nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    # Relationship with Course
    course = db.relationship('Course', backref=db.backref('supplementary_content', lazy=True, cascade="all, delete-orphan"))


class StudentDoubt(db.Model):
    __tablename__ = "StudentDoubt"
    
    doubt_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    doubt_text = db.Column(db.Text, nullable=False)
    video_title = db.Column(db.String(255), nullable=False)  # Changed from video_id
    
    # Foreign key relationship with User model
    # user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    
    # Store student details
    student_name = db.Column(db.String(255), nullable=False)  # New field for name
    student_email = db.Column(db.String(255), nullable=False)  # New field for email
    
    # Relationship with User model
    # student = db.relationship('User', backref=db.backref('doubts', lazy=True))

class DoubtReply(db.Model):
    __tablename__ = 'DoubtReply'
    reply_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    doubt_id = db.Column(
        db.Integer,
        db.ForeignKey('StudentDoubt.doubt_id', name='fk_doubtreply_doubt_id'),  # Explicitly name the foreign key
        nullable=False
    )
    reply = db.Column(db.Text, nullable=False)
    seen = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    
    # Relationship with StudentDoubt
    doubt = db.relationship('StudentDoubt', backref=db.backref('replies', lazy=True, cascade="all, delete-orphan"))

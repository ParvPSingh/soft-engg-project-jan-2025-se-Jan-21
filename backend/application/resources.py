import os
from flask import Flask, request, jsonify
from flask_restful import Resource, fields, marshal_with, reqparse, Api
from application.database import db
from application.models import User, Role, Course, Enrollment, SupplementaryContent, InstructorAlloted, Lecture, Assignment, QA, ProgQA, Scores, Queries, Feedback, KnowledgeBase, StudentDoubt, DoubtReply
from application.validation import ValidationError
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, auth_required, roles_required, roles_accepted, login_required, logout_user
from werkzeug.utils import secure_filename
from application.sec import datastore
from flask import jsonify
from flask_security import current_user
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
api = Api(app)
api=Api()

# Enable CORS for the Flask app
CORS(app)

user_out_fields={
    "id": fields.Integer, 
    "name": fields.String, 
    "email": fields.String, 
    "password": fields.String, 
    "active": fields.Boolean, 
    "fs_uniquifier":fields.String, 
    "roles":fields.List(fields.String)
    }

course_out_fields = {
    "course_id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "instructor_id": fields.Integer
}

lecture_out_fields = {
    "lecture_id": fields.Integer,
    "course_id": fields.Integer,
    "title": fields.String,
    "video_link": fields.String,
    "lecture_no": fields.Integer,
    "week_no": fields.Integer,
    "created_at": fields.DateTime
}

assignment_out_fields = {
    "assignment_id": fields.Integer,
    "course_id": fields.Integer,
    "assignment_no": fields.Integer,
    "week_no": fields.Integer,
    "created_at": fields.DateTime
}

qa_out_fields = {
    "q_id": fields.Integer,
    "qa_assignment_id": fields.Integer,
    "options": fields.String,
    "answer": fields.String
}

prog_qa_out_fields = {
    "q_id": fields.Integer,
    "qa_assignment_id": fields.Integer,
    "options": fields.String,
    "answer": fields.String
}

enrollment_out_fields = {
    "enrollment_id": fields.Integer,
    "course_id": fields.Integer,
    "student_id": fields.Integer,
    "enrollment_date": fields.DateTime
}

feedback_out_fields = {
    "feed_id": fields.Integer,
    "feed_course_id": fields.Integer,
    "feed_user_id": fields.Integer,
    "feed_rating": fields.Integer,
    "feed_content": fields.String,
    "created_at": fields.DateTime
}

knowledgebase_out_fields = {
    "kb_id": fields.Integer,
    "kb_name": fields.String,
    "kb_type": fields.String,
    "kb_location": fields.String,
    "created_at": fields.DateTime
}

scores_out_fields = {
    "score_id": fields.Integer,
    "score_user_id": fields.Integer,
    "week_no": fields.Integer,
    "score": fields.Integer
}

create_user_parser=reqparse.RequestParser()
create_user_parser.add_argument("id")
create_user_parser.add_argument("name")
create_user_parser.add_argument("email")
create_user_parser.add_argument("password")
create_user_parser.add_argument("active")
create_user_parser.add_argument("fs_uniquifier")

create_course_parser = reqparse.RequestParser()
create_course_parser.add_argument("name", type=str, required=True, help="Course name is required")
create_course_parser.add_argument("description", type=str)
create_course_parser.add_argument("instructor_id", type=int, required=True, help="Instructor ID is required")
update_course_parser = reqparse.RequestParser()
update_course_parser.add_argument("name", type=str, required=True, help="Course name is required")
update_course_parser.add_argument("description", type=str)
update_course_parser.add_argument("instructor_id", type=int, required=True, help="Instructor ID is required")

create_lecture_parser = reqparse.RequestParser()
create_lecture_parser.add_argument("course_id", type=int, required=True, help="Course ID is required")
create_lecture_parser.add_argument("title", type=str, required=True, help="Lecture title is required")
create_lecture_parser.add_argument("video_link", type=str, required=True, help="Video link is required")
create_lecture_parser.add_argument("lecture_no", type=int, required=True, help="Lecture number is required")
create_lecture_parser.add_argument("week_no", type=int, required=True, help="Week number is required")
update_lecture_parser = reqparse.RequestParser()
update_lecture_parser.add_argument("title", type=str, required=True, help="Lecture title is required")
update_lecture_parser.add_argument("video_link", type=str, required=True, help="Video link is required")
update_lecture_parser.add_argument("lecture_no", type=int, required=True, help="Lecture number is required")
update_lecture_parser.add_argument("week_no", type=int, required=True, help="Week number is required")

create_assignment_parser = reqparse.RequestParser()
create_assignment_parser.add_argument("course_id", type=int, required=True, help="Course ID is required")
create_assignment_parser.add_argument("assignment_no", type=int, required=True, help="Assignment number is required")
create_assignment_parser.add_argument("week_no", type=int, required=True, help="Week number is required")
update_assignment_parser = reqparse.RequestParser()
update_assignment_parser.add_argument("course_id", type=int, required=True, help="Course ID is required")
update_assignment_parser.add_argument("assignment_no", type=int, required=True, help="Assignment number is required")
update_assignment_parser.add_argument("week_no", type=int, required=True, help="Week number is required")

create_qa_parser = reqparse.RequestParser()
create_qa_parser.add_argument("qa_assignment_id", type=int, required=True, help="Assignment ID is required")
create_qa_parser.add_argument("options", type=str)
create_qa_parser.add_argument("answer", type=str, required=True, help="Answer is required")
update_qa_parser = reqparse.RequestParser()
update_qa_parser.add_argument("options", type=str)
update_qa_parser.add_argument("answer", type=str, required=True, help="Answer is required")

create_prog_qa_parser = reqparse.RequestParser()
create_prog_qa_parser.add_argument("qa_assignment_id", type=int, required=True, help="Assignment ID is required")
create_prog_qa_parser.add_argument("options", type=str)
create_prog_qa_parser.add_argument("answer", type=str, required=True, help="Answer is required")
update_prog_qa_parser = reqparse.RequestParser()
update_prog_qa_parser.add_argument("options", type=str)
update_prog_qa_parser.add_argument("answer", type=str, required=True, help="Answer is required")

create_enrollment_parser = reqparse.RequestParser()
create_enrollment_parser.add_argument("course_id", type=int, required=True, help="Course ID is required")
create_enrollment_parser.add_argument("user_id", type=int, required=True, help="Student ID is required")

create_feedback_parser = reqparse.RequestParser()
create_feedback_parser.add_argument("feed_course_id", type=int, required=True, help="Course ID is required")
create_feedback_parser.add_argument("feed_user_id", type=int, required=True, help="User ID is required")
create_feedback_parser.add_argument("feed_rating", type=int, required=True, help="Rating is required")
create_feedback_parser.add_argument("feed_content", type=str, required=True, help="Content is required")

create_knowledgebase_parser = reqparse.RequestParser()
create_knowledgebase_parser.add_argument("kb_name", type=str, required=True, help="Name is required")
create_knowledgebase_parser.add_argument("kb_type", type=str, required=True, help="Type is required")
create_knowledgebase_parser.add_argument("kb_location", type=str, required=True, help="Location is required")

genai_concept_parser = reqparse.RequestParser()
genai_concept_parser.add_argument("concept", type=str, required=True, 
                                help="Concept name is required")
genai_concept_parser.add_argument("context", type=str)
genai_concept_parser.add_argument("difficulty", type=str, required=True,
                                choices=('beginner','intermediate','advanced'))

genai_plan_parser = reqparse.RequestParser()
genai_plan_parser.add_argument("user_id", type=str, required=True)
genai_plan_parser.add_argument("course_performance", type=dict, required=True)

code_assistant_parser = reqparse.RequestParser()
code_assistant_parser.add_argument("code_snippet", type=str, required=True)
code_assistant_parser.add_argument("error_details", type=str)

create_scores_parser = reqparse.RequestParser()
create_scores_parser.add_argument("score_user_id", type=int, required=True, help="User ID is required")
create_scores_parser.add_argument("week_no", type=int, required=True, help="Week number is required")
create_scores_parser.add_argument("score", type=int, required=True, help="Score is required")


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    datastore.create_user(name=name, email=email, password=hashed_password, roles=['Student'])
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# Login route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email:
        return jsonify({"error_message": "email is not provided"}), 400
    if not password:
        return jsonify({"error_message": "password is not provided"}), 400

    user = datastore.find_user(email=email)

    if not user:
        return jsonify({"error_message": "User was Not Found"}), 404

    # Explicitly check if the user is active
    if not bool(user.active):  # Ensure `active` is interpreted as a boolean
        return jsonify({"error_message": "Your account is inactive. Please contact the admin."}), 401

    if check_password_hash(user.password, password):
        return jsonify({
            "name": user.name,
            "token": user.get_auth_token(),
            "email": user.email,
            "role": user.roles[0].name,
            "user_id": user.user_id,
            "active": user.active
        })
    else:
        return jsonify({"error_message": "Wrong Password"}), 400

# Logout route
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200

class UserAPI(Resource):
    @marshal_with(user_out_fields)
    @auth_required("token")
    @roles_required("Instructor")
    def get(self, username):
        now_user=User.query.filter_by(name=username).first()
        if now_user:
            return now_user, 200
        else:
            raise ValidationError(status_code=404, error_code="UVE1001", error_message="user doesn't exist")

    @marshal_with(user_out_fields)
    def post(self):
        args=create_user_parser.parse_args()
        name=args.get("name", None)
        email=args.get("email",None)
        password=args.get("password",None)
        print(name)
        print(email)
        print(password)
        if "@" not in email:
            raise ValidationError(status_code=400, error_code="UVE1006", error_message="Not a valid email")
        if len(password)<7:
            raise ValidationError(status_code=400, error_code="UVE1007", error_message="Password should have atleast 8 letters")
        if name is None:
            raise ValidationError(status_code=400, error_code="UVE1002", error_message="username is required")
        if password is None:
            raise ValidationError(status_code=400, error_code="UVE1003", error_message="password is required")
        
        now_user_name=User.query.filter_by(name=name).first()
        if now_user_name:
            raise ValidationError(status_code=400, error_code="UVE1004", error_message="duplicate username")
        
        if not datastore.find_user(email=email):
            new_user=datastore.create_user(name=name, email=email, password=generate_password_hash(password, method="pbkdf2:sha256"), roles=['Student'])
        db.session.commit()

        return new_user, 201


class CourseAPI(Resource):
    @marshal_with(course_out_fields)
    @auth_required("token")
    @roles_required("Instructor")
    def get(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            raise ValidationError(status_code=404, error_code="CVE1001", error_message="Course not found")
        return course, 200

    @marshal_with(course_out_fields)
    @auth_required("token")
    @roles_required("Instructor")
    def post(self):
        args = create_course_parser.parse_args()
        name = args.get("name")
        description = args.get("description")
        instructor_id = args.get("instructor_id")

        if name is None:
            raise ValidationError(status_code=400, error_code="CVE1002", error_message="Course name is required")
        if instructor_id is None:
            raise ValidationError(status_code=400, error_code="CVE1003", error_message="Instructor ID is required")

        new_course = Course(name=name, description=description, instructor_id=instructor_id)
        db.session.add(new_course)
        db.session.commit()
        return new_course, 201

    @marshal_with(course_out_fields)
    @auth_required("token")
    @roles_required("Instructor")
    def put(self, course_id):
        args = create_course_parser.parse_args()
        name = args.get("name")
        description = args.get("description")
        instructor_id = args.get("instructor_id")

        if name is None:
            raise ValidationError(status_code=400, error_code="CVE1002", error_message="Course name is required")
        if instructor_id is None:
            raise ValidationError(status_code=400, error_code="CVE1003", error_message="Instructor ID is required")

        course = Course.query.get(course_id)
        if not course:
            raise ValidationError(status_code=404, error_code="CVE1001", error_message="Course not found")

        course.name = name
        course.description = description
        course.instructor_id = instructor_id
        db.session.commit()
        return course, 200

    @auth_required("token")
    @roles_required("Instructor")
    def delete(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            raise ValidationError(status_code=404, error_code="CVE1001", error_message="Course not found")
        db.session.delete(course)
        db.session.commit()
        return "", 204
    
class LectureAPI(Resource):
    @marshal_with(lecture_out_fields)
    @auth_required("token")
    def get(self, lecture_id):
        lecture = Lecture.query.get(lecture_id)
        if not lecture:
            raise ValidationError(status_code=404, error_code="LVE1001", error_message="Lecture not found")
        return lecture, 201
    
    @marshal_with(lecture_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def post(self):
        args = create_lecture_parser.parse_args()
        course_id = args.get("course_id")
        title = args.get("title")
        video_link = args.get("video_link")
        lecture_no = args.get("lecture_no")
        week_no = args.get("week_no")
        created_at = datetime.today()

        if course_id is None:
            raise ValidationError(status_code=400, error_code="LVE1002", error_message="Course ID is required")
        if title is None:
            raise ValidationError(status_code=400, error_code="LVE1003", error_message="Title is required")
        if video_link is None:
            raise ValidationError(status_code=400, error_code="LVE1004", error_message="Video link is required")
        if lecture_no is None:
            raise ValidationError(status_code=400, error_code="LVE1005", error_message="Lecture number is required")
        if week_no is None:
            raise ValidationError(status_code=400, error_code="LVE1006", error_message="Week number is required")

        new_lecture = Lecture(course_id=course_id, title=title, video_link=video_link,
                              lecture_no=lecture_no, week_no=week_no, created_at=created_at)
        db.session.add(new_lecture)
        db.session.commit()
        return new_lecture, 201
    
    @marshal_with(lecture_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def put(self, lecture_id):
        args = create_lecture_parser.parse_args()
        course_id = args.get("course_id")
        title = args.get("title")
        video_link = args.get("video_link")
        lecture_no = args.get("lecture_no")
        week_no = args.get("week_no")

        if course_id is None:
            raise ValidationError(status_code=400, error_code="LVE1002", error_message="Course ID is required")
        if title is None:
            raise ValidationError(status_code=400, error_code="LVE1003", error_message="Title is required")
        if video_link is None:
            raise ValidationError(status_code=400, error_code="LVE1004", error_message="Video link is required")
        if lecture_no is None:
            raise ValidationError(status_code=400, error_code="LVE1005", error_message="Lecture number is required")
        if week_no is None:
            raise ValidationError(status_code=400, error_code="LVE1006", error_message="Week number is required")

        new_lecture = Lecture.query.filter_by(lecture_id=lecture_id).first()
        new_lecture.course_id=course_id
        new_lecture.title=title
        new_lecture.video_link=video_link
        new_lecture.lecture_no=lecture_no
        new_lecture.week_no=week_no
        db.session.commit()
        return new_lecture, 201
    
    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def delete(self, lecture_id):
        now_lec=Lecture.query.filter_by(lecture_id=lecture_id).first()
        if now_lec is None:
            raise ValidationError(status_code=404, error_code="LVE1001", error_message="Lecture doesn't exist")
        db.session.delete(now_lec)
        db.session.commit()
        return "", 200

class AssignmentAPI(Resource):
    @marshal_with(assignment_out_fields)
    @auth_required("token")
    def get(self, assignment_id):
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            raise ValidationError(status_code=404, error_code="AVE1001", error_message="Assignment not found")
        return assignment, 200
    
    @marshal_with(assignment_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def post(self):
        args = create_assignment_parser.parse_args()
        course_id = args.get("course_id")
        assignment_no = args.get("assignment_no")
        week_no = args.get("week_no")
        created_at = datetime.today()

        if course_id is None:
            raise ValidationError(status_code=400, error_code="AVE1002", error_message="Course ID is required")
        if assignment_no is None:
            raise ValidationError(status_code=400, error_code="AVE1003", error_message="Assignment number is required")
        if week_no is None:
            raise ValidationError(status_code=400, error_code="AVE1004", error_message="Week number is required")

        new_assignment = Assignment(course_id=course_id, assignment_no=assignment_no, week_no=week_no, created_at=created_at)
        db.session.add(new_assignment)
        db.session.commit()
        return new_assignment, 201

    @marshal_with(assignment_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def put(self, assignment_id):
        args = create_assignment_parser.parse_args()
        course_id = args.get("course_id")
        assignment_no = args.get("assignment_no")
        week_no = args.get("week_no")

        if course_id is None:
            raise ValidationError(status_code=400, error_code="AVE1002", error_message="Course ID is required")
        if assignment_no is None:
            raise ValidationError(status_code=400, error_code="AVE1003", error_message="Assignment number is required")
        if week_no is None:
            raise ValidationError(status_code=400, error_code="AVE1004", error_message="Week number is required")

        assignment = Assignment.query.filter_by(assignment_id=assignment_id).first()
        if not assignment:
            raise ValidationError(status_code=404, error_code="AVE1001", error_message="Assignment not found")
        
        assignment.course_id = course_id
        assignment.assignment_no = assignment_no
        assignment.week_no = week_no
        db.session.commit()
        return assignment, 200

    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def delete(self, assignment_id):
        assignment = Assignment.query.filter_by(assignment_id=assignment_id).first()
        if not assignment:
            raise ValidationError(status_code=404, error_code="AVE1001", error_message="Assignment not found")
        db.session.delete(assignment)
        db.session.commit()
        return "", 204

class QAAPI(Resource):
    @marshal_with(qa_out_fields)
    @auth_required("token")
    def get(self, q_id):
        qa = QA.query.get(q_id)
        if not qa:
            raise ValidationError(status_code=404, error_code="QVE1001", error_message="QA not found")
        return qa, 200

    @marshal_with(qa_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def post(self):
        args = create_qa_parser.parse_args()
        qa_assignment_id = args.get("qa_assignment_id")
        options = args.get("options")
        answer = args.get("answer")

        if qa_assignment_id is None:
            raise ValidationError(status_code=400, error_code="QVE1002", error_message="Assignment ID is required")
        if options is None:
            raise ValidationError(status_code=400, error_code="QVE1003", error_message="Options are required")
        if answer is None:
            raise ValidationError(status_code=400, error_code="QVE1004", error_message="Answer is required")

        new_qa = QA(qa_assignment_id=qa_assignment_id, options=options, answer=answer)
        db.session.add(new_qa)
        db.session.commit()
        return new_qa, 201

    @marshal_with(qa_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def put(self, q_id):
        args = create_qa_parser.parse_args()
        qa_assignment_id = args.get("qa_assignment_id")
        options = args.get("options")
        answer = args.get("answer")

        if qa_assignment_id is None:
            raise ValidationError(status_code=400, error_code="QVE1002", error_message="Assignment ID is required")
        if options is None:
            raise ValidationError(status_code=400, error_code="QVE1003", error_message="Options are required")
        if answer is None:
            raise ValidationError(status_code=400, error_code="QVE1004", error_message="Answer is required")

        qa = QA.query.filter_by(q_id=q_id).first()
        if not qa:
            raise ValidationError(status_code=404, error_code="QVE1001", error_message="QA not found")
        
        qa.qa_assignment_id = qa_assignment_id
        qa.options = options
        qa.answer = answer
        db.session.commit()
        return qa, 200

    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def delete(self, q_id):
        qa = QA.query.filter_by(q_id=q_id).first()
        if not qa:
            raise ValidationError(status_code=404, error_code="QVE1001", error_message="QA not found")
        db.session.delete(qa)
        db.session.commit()
        return "", 204

class ProgQAAPI(Resource):
    @marshal_with(prog_qa_out_fields)
    @auth_required("token")
    def get(self, prog_q_id):
        qa = ProgQA.query.get(prog_q_id)
        if not qa:
            raise ValidationError(status_code=404, error_code="QVE1001", error_message="ProgQA not found")
        return qa, 200

    @marshal_with(prog_qa_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def post(self):
        args = create_qa_parser.parse_args()
        prog_qa_assignment_id = args.get("prog_qa_assignment_id")
        prog_options = args.get("prog_options")
        prog_answer = args.get("prog_answer")

        if prog_qa_assignment_id is None:
            raise ValidationError(status_code=400, error_code="QVE1002", error_message="Prog Assignment ID is required")
        if prog_options is None:
            raise ValidationError(status_code=400, error_code="QVE1003", error_message="Options are required")
        if prog_answer is None:
            raise ValidationError(status_code=400, error_code="QVE1004", error_message="Answer is required")

        new_qa = ProgQA(qa_assignment_id=prog_qa_assignment_id, prog_options=prog_options, prog_answer=prog_answer)
        db.session.add(new_qa)
        db.session.commit()
        return new_qa, 201

    @marshal_with(prog_qa_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def put(self, prog_q_id):
        args = create_qa_parser.parse_args()
        prog_qa_assignment_id = args.get("prog_qa_assignment_id")
        prog_options = args.get("prog_options")
        prog_answer = args.get("prog_answer")

        if prog_qa_assignment_id is None:
            raise ValidationError(status_code=400, error_code="QVE1002", error_message="Prog Assignment ID is required")
        if prog_options is None:
            raise ValidationError(status_code=400, error_code="QVE1003", error_message="Options are required")
        if prog_answer is None:
            raise ValidationError(status_code=400, error_code="QVE1004", error_message="Answer is required")

        prog_qa = QA.query.filter_by(prog_q_id=prog_q_id).first()
        if not prog_qa:
            raise ValidationError(status_code=404, error_code="QVE1001", error_message="QA not found")
        
        prog_qa.qa_assignment_id = prog_qa_assignment_id
        prog_qa.options = prog_options
        prog_qa.answer = prog_answer
        db.session.commit()
        return prog_qa, 200

    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def delete(self, prog_q_id):
        prog_qa = ProgQA.query.filter_by(prog_q_id=prog_q_id).first()
        if not prog_qa:
            raise ValidationError(status_code=404, error_code="QVE1001", error_message="QA not found")
        db.session.delete(prog_qa)
        db.session.commit()
        return "", 204

class EnrollmentAPI(Resource):
    @marshal_with(enrollment_out_fields)
    
    def get(self, enrollment_id):
        enrollment = Enrollment.query.filter_by(enrollment_id=enrollment_id).first()
        if not enrollment:
            raise ValidationError(status_code=404, error_code="EVE1001", error_message="Enrollment not found")
        return enrollment, 200

    @marshal_with(enrollment_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def post(self):
        args = create_enrollment_parser.parse_args()
        course_id = args.get("course_id")
        # Change this line to match the parser parameter name
        user_id = args.get("user_id")  # Changed from student_id to user_id
        enrollment_date = datetime.today()

        # Add validation to check if course exists
        course = Course.query.get(course_id)
        if not course:
            raise ValidationError(status_code=404, error_code="EVE1004", error_message="Course not found")

        # Add validation to check if student exists
        student = User.query.get(user_id)  # Changed from student_id to user_id
        if not student:
            raise ValidationError(status_code=404, error_code="EVE1005", error_message="Student not found")

        # Check if enrollment already exists
        existing_enrollment = Enrollment.query.filter_by(
            course_id=course_id,
            student_id=user_id  # Changed from student_id to user_id
        ).first()
        if existing_enrollment:
            raise ValidationError(status_code=400, error_code="EVE1006", error_message="Student already enrolled in this course")

        new_enrollment = Enrollment(course_id=course_id, student_id=user_id, enrollment_date=enrollment_date)  # Changed from student_id to user_id
        db.session.add(new_enrollment)
        db.session.commit()
        return new_enrollment, 201

    @marshal_with(enrollment_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def put(self, enrollment_id):
        args = create_enrollment_parser.parse_args()
        course_id = args.get("course_id")
        student_id = args.get("student_id")

        if course_id is None:
            raise ValidationError(status_code=400, error_code="EVE1002", error_message="Course ID is required")
        if student_id is None:
            raise ValidationError(status_code=400, error_code="EVE1003", error_message="Student ID is required")

        enrollment = Enrollment.query.filter_by(enrollment_id=enrollment_id).first()
        if not enrollment:
            raise ValidationError(status_code=404, error_code="EVE1001", error_message="Enrollment not found")
        
        enrollment.course_id = course_id
        enrollment.student_id = student_id
        db.session.commit()
        return enrollment, 200

    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def delete(self, enrollment_id):
        enrollment = Enrollment.query.filter_by(enrollment_id=enrollment_id).first()
        if not enrollment:
            raise ValidationError(status_code=404, error_code="EVE1001", error_message="Enrollment not found")
        db.session.delete(enrollment)
        db.session.commit()
        return "", 204
class FeedbackListAPI(Resource):
    @marshal_with(feedback_out_fields)
    
    def get(self):
        feedbacks = Feedback.query.all()
        if not feedbacks:
            raise ValidationError(status_code=404, error_code="FVE1006", error_message="No feedbacks found")
        return feedbacks, 200

# Add the new endpoint
api.add_resource(FeedbackListAPI, "/api/feedback/full")

class FeedbackAPI(Resource):
    @marshal_with(feedback_out_fields)

    def get(self, feed_id):
        feedback = Feedback.query.filter_by(feed_id=feed_id).first()
        if not feedback:
            raise ValidationError(status_code=404, error_code="FVE1001", error_message="Feedback not found")
        return feedback, 200

    @marshal_with(feedback_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def post(self):
        args = create_feedback_parser.parse_args()
        feed_course_id = args.get("feed_course_id")
        feed_user_id = args.get("feed_user_id")
        feed_rating = args.get("feed_rating")
        feed_content = args.get("feed_content")

        if feed_course_id is None:
            raise ValidationError(status_code=400, error_code="FVE1002", error_message="Course ID is required")
        if feed_user_id is None:
            raise ValidationError(status_code=400, error_code="FVE1003", error_message="User ID is required")
        if feed_rating is None:
            raise ValidationError(status_code=400, error_code="FVE1004", error_message="Rating is required")
        if feed_content is None:
            raise ValidationError(status_code=400, error_code="FVE1005", error_message="Feedback content is required")

        new_feedback = Feedback(feed_course_id=feed_course_id, feed_user_id=feed_user_id,
                                feed_rating=feed_rating, feed_content=feed_content)
        db.session.add(new_feedback)
        db.session.commit()
        return new_feedback, 201

    @marshal_with(feedback_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def put(self, feed_id):
        args = create_feedback_parser.parse_args()
        feed_course_id = args.get("feed_course_id")
        feed_user_id = args.get("feed_user_id")
        feed_rating = args.get("feed_rating")
        feed_content = args.get("feed_content")

        if feed_course_id is None:
            raise ValidationError(status_code=400, error_code="FVE1002", error_message="Course ID is required")
        if feed_user_id is None:
            raise ValidationError(status_code=400, error_code="FVE1003", error_message="User ID is required")
        if feed_rating is None:
            raise ValidationError(status_code=400, error_code="FVE1004", error_message="Rating is required")
        if feed_content is None:
            raise ValidationError(status_code=400, error_code="FVE1005", error_message="Feedback content is required")

        feedback = Feedback.query.filter_by(feed_id=feed_id).first()
        if not feedback:
            raise ValidationError(status_code=404, error_code="FVE1001", error_message="Feedback not found")
        
        feedback.feed_course_id = feed_course_id
        feedback.feed_user_id = feed_user_id
        feedback.feed_rating = feed_rating
        feedback.feed_content = feed_content
        db.session.commit()
        return feedback, 200

    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def delete(self, feed_id):
        feedback = Feedback.query.filter_by(feed_id=feed_id).first()
        if not feedback:
            raise ValidationError(status_code=404, error_code="FVE1001", error_message="Feedback not found")
        db.session.delete(feedback)
        db.session.commit()
        return "", 204

class KnowledgeBaseAPI(Resource):
    @marshal_with(knowledgebase_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor")
    def get(self, kb_id):
        kb = KnowledgeBase.query.filter_by(kb_id=kb_id).first()
        if not kb:
            raise ValidationError(status_code=404, error_code="KVE1001", error_message="KnowledgeBase entry not found")
        return kb, 200

    @marshal_with(knowledgebase_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor")
    def post(self):
        args = create_knowledgebase_parser.parse_args()
        kb_name = args.get("kb_name")
        kb_type = args.get("kb_type")
        kb_location = args.get("kb_location")

        if kb_name is None:
            raise ValidationError(status_code=400, error_code="KVE1002", error_message="Knowledge Base name is required")
        if kb_type is None:
            raise ValidationError(status_code=400, error_code="KVE1003", error_message="Knowledge Base type is required")
        if kb_location is None:
            raise ValidationError(status_code=400, error_code="KVE1004", error_message="Knowledge Base location is required")

        new_kb = KnowledgeBase(kb_name=kb_name, kb_type=kb_type, kb_location=kb_location)
        db.session.add(new_kb)
        db.session.commit()
        return new_kb, 201

    @marshal_with(knowledgebase_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor")
    def put(self, kb_id):
        args = create_knowledgebase_parser.parse_args()
        kb_name = args.get("kb_name")
        kb_type = args.get("kb_type")
        kb_location = args.get("kb_location")

        if kb_name is None:
            raise ValidationError(status_code=400, error_code="KVE1002", error_message="Knowledge Base name is required")
        if kb_type is None:
            raise ValidationError(status_code=400, error_code="KVE1003", error_message="Knowledge Base type is required")
        if kb_location is None:
            raise ValidationError(status_code=400, error_code="KVE1004", error_message="Knowledge Base location is required")

        kb = KnowledgeBase.query.filter_by(kb_id=kb_id).first()
        if not kb:
            raise ValidationError(status_code=404, error_code="KVE1001", error_message="KnowledgeBase entry not found")
        
        kb.kb_name = kb_name
        kb.kb_type = kb_type
        kb.kb_location = kb_location
        db.session.commit()
        return kb, 200

    @auth_required("token")
    @roles_accepted("Instructor")
    def delete(self, kb_id):
        kb = KnowledgeBase.query.filter_by(kb_id=kb_id).first()
        if not kb:
            raise ValidationError(status_code=404, error_code="KVE1001", error_message="KnowledgeBase entry not found")
        db.session.delete(kb)
        db.session.commit()
        return "", 204


class GenAIConceptExplainerAPI(Resource):
    @auth_required("token")
    @roles_accepted("Student", "Instructor", "TA")
    def post(self):
        args = genai_concept_parser.parse_args()
        # Integrate with KnowledgeBase model
        kb_resources = KnowledgeBase.query.filter(
            KnowledgeBase.kb_name.ilike(f"%{args['concept']}%")
        ).limit(3).all()
        
        return {
            "explanation": f"AI-generated explanation of {args['concept']} for {args['difficulty']} level",
            "related_resources": [resource.kb_location for resource in kb_resources]
        }, 200

class GenAILearningPlanAPI(Resource):
    @auth_required("token")
    @roles_accepted("Student", "Instructor")
    def post(self):
        args = genai_plan_parser.parse_args()
        # Use Scores model for personalization
        scores = Scores.query.filter_by(query_student_id=args['user_id']).all()
        
        return {
            "weekly_schedule": [
                f"Week {i}: Focus on {topic}" 
                for i, topic in enumerate(['Foundations', 'Applications', 'Advanced Concepts'], 1)
            ],
            "performance_analysis": {s.query_assignment_id: s.score for s in scores}
        }, 200

class GenAICodeAssistantAPI(Resource):
    @auth_required("token")
    @roles_accepted("Student")
    def post(self):
        args = code_assistant_parser.parse_args()
        # Connect with ProgQA model
        similar_errors = ProgQA.query.filter(
            ProgQA.prog_answer.ilike(f"%{args['error_details']}%")
        ).limit(2).all()
        
        return {
            "improvements": [
                "Fix syntax error in line 45",
                "Optimize database query"
            ],
            "similar_problems": [qa.prog_options for qa in similar_errors]
        }, 200

class ConversationAPI(Resource):
    @auth_required("token")
    def post(self):
        new_thread = {
            "thread_id": f"THREAD_{datetime.utcnow().timestamp()}",
            "created_at": datetime.utcnow().isoformat()
        }
        return new_thread, 201

    @auth_required("token")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("thread_id", required=True, location='args')
        args = parser.parse_args()
        
        # Sample implementation using Queries model
        history = Queries.query.filter_by(
            query_student_id=current_user.user_id
        ).order_by(Queries.created_at.desc()).limit(5).all()
        
        return [{
            "query": q.description,
            "timestamp": q.created_at.isoformat()
        } for q in history], 200

class ScoresAPI(Resource):
    @marshal_with(scores_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def get(self, score_id):
        score = Scores.query.get(score_id)
        if not score:
            raise ValidationError(status_code=404, error_code="SVE1001", error_message="Score not found")
        return score, 200

    @marshal_with(scores_out_fields)
    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def post(self):
        args = create_scores_parser.parse_args()
        score_user_id = args.get("score_user_id")
        week_no = args.get("week_no")
        score = args.get("score")

        # Validate student exists
        student = User.query.get(score_user_id)
        if not student:
            raise ValidationError(status_code=404, error_code="SVE1002", error_message="Student not found")

        # Validate week number
        if week_no < 0:
            raise ValidationError(status_code=400, error_code="SVE1003", error_message="Week number cannot be negative")

        # Create new score
        new_score = Scores(
            score_user_id=score_user_id,
            week_no=week_no,
            score=score
        )
        db.session.add(new_score)
        db.session.commit()
        return new_score, 201

    @auth_required("token")
    @roles_accepted("Instructor", "TA")
    def delete(self, score_id):
        score = Scores.query.get(score_id)
        if not score:
            raise ValidationError(status_code=404, error_code="SVE1001", error_message="Score not found")
        db.session.delete(score)
        db.session.commit()
        return "", 204

#Om added:
class MyCoursesAPI(Resource):
    @auth_required("token")
    def get(self):
        print(f"Current User: {current_user}")  # Debugging line
        if not current_user:
            return {"message": "Unauthorized: User not found"}, 401

        student_id = current_user.user_id
        enrollments = Enrollment.query.filter_by(student_id=student_id).all()
        if not enrollments:
            return {"message": "No enrolled courses found"}, 404

        courses = [{"course_id": e.course.course_id, "name": e.course.name} for e in enrollments]
        return courses, 200


UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'pdf'}

# Flask Config
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define API response fields
supplementary_out_fields = {
    "id": fields.Integer,
    "course_id": fields.Integer,
    "week_no": fields.Integer,
    "file_name": fields.String,
    "file_url": fields.String
}

class SupplementaryContentAPI(Resource):

    @marshal_with(supplementary_out_fields)
    def get(self, course_id, week_no):
        """Fetch supplementary materials for a specific course & week"""
        materials = SupplementaryContent.query.filter_by(course_id=course_id, week_no=week_no).all()
        if not materials:
            return {"message": "No supplementary content found"}, 404
        return materials, 200

    
    
    def post(self):
        """Upload a supplementary PDF"""
        course_id = request.form.get("course_id")
        week_no = request.form.get("week_no")

        if not course_id or not week_no:
            return {"error": "Course ID and Week number are required"}, 400

        if 'file' not in request.files:
            return {"error": "No file provided"}, 400
        
        file = request.files['file']
        if file.filename == '':
            return {"error": "No selected file"}, 400

        # Validate file type
        if file and file.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Store relative path in DB
            new_content = SupplementaryContent(
                course_id=int(course_id),
                week_no=int(week_no),
                file_name=filename,
                file_url=f"/static/uploads/{filename}"  # Relative URL
            )
            db.session.add(new_content)
            db.session.commit()

            return {"message": "File uploaded successfully", "file_url": new_content.file_url}, 201
        else:
            return {"error": "Invalid file format"}, 400

    
   
    def delete(self, pdf_id):
        """Delete a supplementary PDF"""
        file_entry = SupplementaryContent.query.filter_by(id=pdf_id).first()
        if not file_entry:
            return {"error": "File not found"}, 404

        # Remove from filesystem
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_entry.file_name)
        if os.path.exists(file_path):
            os.remove(file_path)

        # Remove from database
        db.session.delete(file_entry)
        db.session.commit()
        
        return {"message": "File deleted successfully"}, 200




api.add_resource(UserAPI, "/api/user/<string:username>", "/api/user")
api.add_resource(CourseAPI, "/api/course/<int:course_id>", "/api/course")
api.add_resource(LectureAPI, "/api/lecture/<int:lecture_id>", "/api/lecture")
api.add_resource(AssignmentAPI, "/api/assignment/<int:assignment_id>", "/api/assignment")
api.add_resource(QAAPI, "/api/qas/<int:q_id>", "/api/qas")
api.add_resource(EnrollmentAPI, "/api/enrollment/<int:enrollment_id>", "/api/enrollment")
api.add_resource(FeedbackAPI, "/api/feedback/<int:feed_id>", "/api/feedback")
api.add_resource(KnowledgeBaseAPI, "/api/knowledgebase/<int:kb_id>", "/api/knowledgebase")
api.add_resource(GenAIConceptExplainerAPI, '/genai/concept_explainer')
api.add_resource(GenAILearningPlanAPI, '/genai/learning_plan')
api.add_resource(GenAICodeAssistantAPI, '/genai/code_assistant')
api.add_resource(ConversationAPI, '/conversations/context')
api.add_resource(ScoresAPI, "/api/scores", "/api/scores/<int:score_id>")

#added later
api.add_resource(MyCoursesAPI, "/api/mycourses")
api.add_resource(SupplementaryContentAPI, 
    "/api/supplementary",                        # POST: Upload
    "/api/supplementary/<int:course_id>/<int:week_no>",  # GET: Fetch files
    "/api/supplementary/<int:pdf_id>"            # DELETE: Remove file
)

class WeeklyAverageScoresAPI(Resource):
    
    def get(self):
        """
        Compute the average score for each week from the Scores table.
        Returns a dictionary with week numbers as keys and average scores as values.
        """
        # Query all scores from the database
        all_scores = Scores.query.all()
        
        if not all_scores:
            return {"message": "No scores found in the database"}, 404
        
        # Group scores by week
        scores_by_week = {}
        for score in all_scores:
            week = score.week_no
            if week not in scores_by_week:
                scores_by_week[week] = []
            scores_by_week[week].append(score.score)
        
        # Calculate average for each week
        weekly_averages = {}
        for week, scores in scores_by_week.items():
            weekly_averages[week] = sum(scores) / len(scores)
        
        return {
            "weekly_averages": weekly_averages,
            "total_students": len(set(score.score_user_id for score in all_scores)),
            "total_weeks": len(weekly_averages)
        }, 200

# Add the new endpoint
api.add_resource(WeeklyAverageScoresAPI, "/api/weekly-average-scores")

class EnrolledStudentsAPI(Resource):
    def get(self, course_id):
        """
        Fetch all enrolled students for a specific course.
        Returns name, email, and active status of each student.
        """
        enrollments = Enrollment.query.filter_by(course_id=course_id).all()
        if not enrollments:
            return {"message": "No students enrolled in this course"}, 404

        students = [
            {
                "name": enrollment.student.name,
                "email": enrollment.student.email,
                "active": enrollment.student.active
            }
            for enrollment in enrollments
        ]
        return {"students": students}, 200

# Add the new endpoint
api.add_resource(EnrolledStudentsAPI, "/api/enrolled-students/<int:course_id>")

class AllEnrolledStudentsAPI(Resource):
    def get(self):
        """
        Fetch all enrolled students across all courses.
        Returns name, email, user_id, and active status of each student.
        """
        enrollments = Enrollment.query.distinct(Enrollment.student_id).all()  # Ensure no duplicates
        if not enrollments:
            return {"message": "No students enrolled in any course"}, 404

        students = [
            {
                "user_id": enrollment.student.user_id,  # Include user_id
                "name": enrollment.student.name,
                "email": enrollment.student.email,
                "active": enrollment.student.active
            }
            for enrollment in enrollments
        ]
        return {"students": students}, 200

# Add the new endpoint
api.add_resource(AllEnrolledStudentsAPI, "/api/enrolled-students")

class DoubtReplyAPI(Resource):
    def post(self):
        """
        Push a reply from the TA to the DoubtReply table for a doubt in the StudentDoubt table.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("doubt_id", type=int, required=True, help="Doubt ID is required")
        parser.add_argument("reply", type=str, required=True, help="Reply content is required")
        args = parser.parse_args()

        doubt_id = args.get("doubt_id")
        reply = args.get("reply")

        # Validate if the doubt exists
        doubt = StudentDoubt.query.filter_by(doubt_id=doubt_id).first()
        if not doubt:
            raise ValidationError(status_code=404, error_code="DRE1001", error_message="Doubt not found")

        # Create a new reply entry
        new_reply = DoubtReply(doubt_id=doubt_id, reply=reply)
        db.session.add(new_reply)
        db.session.commit()

        return {
            "message": "Reply added successfully",
            "reply_id": new_reply.reply_id,
            "student_name": doubt.student_name,
            "student_email": doubt.student_email
        }, 201

# Update the endpoint
api.add_resource(DoubtReplyAPI, "/api/doubts/reply")

class DoubtReplyFetchAPI(Resource):
    def get(self, doubt_id):
        """
        Fetch the reply for a specific doubt from the DoubtReply table.
        """
        # Validate if the doubt exists
        doubt = StudentDoubt.query.filter_by(doubt_id=doubt_id).first()
        if not doubt:
            raise ValidationError(status_code=404, error_code="DRE1001", error_message="Doubt not found")

        # Fetch the reply for the doubt
        reply = DoubtReply.query.filter_by(doubt_id=doubt_id).first()
        if not reply:
            return {"message": "No reply found for this doubt"}, 404

        return {
            "reply_id": reply.reply_id,
            "reply": reply.reply,
            "created_at": reply.created_at.isoformat()
        }, 200

# Add the new endpoint
api.add_resource(DoubtReplyFetchAPI, "/api/doubts/<int:doubt_id>/reply")

class StudentDoubtAPI(Resource):
    def get(self):
        """
        Fetch all student doubts along with their latest replies (if any).
        """
        doubts = StudentDoubt.query.all()
        result = []
        for doubt in doubts:
            latest_reply = DoubtReply.query.filter_by(doubt_id=doubt.doubt_id).order_by(DoubtReply.created_at.desc()).first()
            result.append({
                "doubt_id": doubt.doubt_id,
                "doubt_text": doubt.doubt_text,
                "video_title": doubt.video_title,
                "student_name": doubt.student_name,
                "student_email": doubt.student_email,
                "reply": latest_reply.reply if latest_reply else None,
                "reply_seen": latest_reply.seen if latest_reply else None  # Include the seen status
            })
        return result, 200

# Add the new endpoint
api.add_resource(StudentDoubtAPI, "/api/student-doubts")

class MarkRepliesAsSeenAPI(Resource):
    def post(self):
        """
        Mark all replies for a specific student as seen.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("student_email", type=str, required=True, help="Student email is required")
        args = parser.parse_args()

        student_email = args.get("student_email")
    
        # Debugging: Log the student email
        print(f"MarkRepliesAsSeenAPI called for student_email: {student_email}")

        # Fetch all doubts for the student
        doubts = StudentDoubt.query.filter_by(student_email=student_email).all()

        if not doubts:
            print(f"No doubts found for student_email: {student_email}")  # Debugging log
            return {"message": "No doubts found for the student"}, 404

        # Debugging: Log the fetched doubts
        print(f"Fetched doubts for {student_email}: {[d.doubt_id for d in doubts]}")

        # Mark all replies as seen
        updated_replies = 0
        for doubt in doubts:
            for reply in doubt.replies:
                if not reply.seen:  # Only update if not already seen
                    reply.seen = True
                    updated_replies += 1

        # Debugging: Log the number of replies updated
        print(f"Updated {updated_replies} replies as seen for {student_email}")

        db.session.commit()
        return {"message": f"All replies marked as seen. Total updated: {updated_replies}"}, 200

# Add the new endpoint
api.add_resource(MarkRepliesAsSeenAPI, "/api/replies/mark-seen")

class BlockStudentAPI(Resource):
    def put(self, user_id):
        """
        Toggle the active status of a student.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("active", type=bool, required=True, help="Active status (true/false) is required")
        args = parser.parse_args()

        active = args.get("active")
        user = User.query.filter_by(user_id=user_id).first()

        if not user:
            return {"error": "User not found"}, 404  # Return a JSON-serializable object

        try:
            user.active = active
            db.session.commit()
            status = "unblocked" if active else "blocked"
            return {"message": f"User successfully {status}", "active": user.active}, 200  # Return JSON
        except Exception as e:
            db.session.rollback()
            return {"error": "An error occurred while updating the user's status"}, 500  # Return JSON

# Add the new endpoint
api.add_resource(BlockStudentAPI, "/api/user/<int:user_id>/block")



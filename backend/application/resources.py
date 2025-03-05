from flask_restful import Resource, fields, marshal_with, reqparse, Api
from application.database import db
from application.models import User, Role, Course, Enrollment, InstructorAlloted, Lecture, Assignment, QA, ProgQA, Scores, Queries, Feedback, KnowledgeBase
from application.validation import ValidationError
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, auth_required, roles_required
from application.sec import datastore
from flask import jsonify
from flask_security import current_user
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

api=Api()

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
create_enrollment_parser.add_argument("student_id", type=int, required=True, help="Student ID is required")

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
    @roles_required("Instructor")
    @roles_required("TA")
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
    @roles_required("Instructor")
    @roles_required("TA")
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
    @roles_required("Instructor")
    @roles_required("TA")
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
    @roles_required("Instructor")
    @roles_required("TA")
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
    @roles_required("Instructor")
    @roles_required("TA")
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
    @roles_required("Instructor")
    @roles_required("TA")
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
    @roles_required("Instructor")
    @roles_required("TA")
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
    @roles_required("Instructor")
    @roles_required("TA")
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
    @roles_required("Instructor")
    @roles_required("TA")
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
    @roles_required("Instructor")
    @roles_required("TA")
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
    @roles_required("Instructor")
    @roles_required("TA")
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
    @roles_required("Instructor")
    @roles_required("TA")
    def delete(self, prog_q_id):
        prog_qa = ProgQA.query.filter_by(prog_q_id=prog_q_id).first()
        if not prog_qa:
            raise ValidationError(status_code=404, error_code="QVE1001", error_message="QA not found")
        db.session.delete(prog_qa)
        db.session.commit()
        return "", 204

class EnrollmentAPI(Resource):
    @marshal_with(enrollment_out_fields)
    @auth_required("token")
    @roles_required("Instructor")
    @roles_required("TA")
    def get(self, enrollment_id):
        enrollment = Enrollment.query.filter_by(enrollment_id=enrollment_id).first()
        if not enrollment:
            raise ValidationError(status_code=404, error_code="EVE1001", error_message="Enrollment not found")
        return enrollment, 200

    @marshal_with(enrollment_out_fields)
    @auth_required("token")
    @roles_required("Instructor")
    @roles_required("TA")
    def post(self):
        args = create_enrollment_parser.parse_args()
        course_id = args.get("course_id")
        student_id = args.get("student_id")

        if course_id is None:
            raise ValidationError(status_code=400, error_code="EVE1002", error_message="Course ID is required")
        if student_id is None:
            raise ValidationError(status_code=400, error_code="EVE1003", error_message="Student ID is required")

        new_enrollment = Enrollment(course_id=course_id, student_id=student_id)
        db.session.add(new_enrollment)
        db.session.commit()
        return new_enrollment, 201

    @marshal_with(enrollment_out_fields)
    @auth_required("token")
    @roles_required("Instructor")
    @roles_required("TA")
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
    @roles_required("Instructor")
    @roles_required("TA")
    def delete(self, enrollment_id):
        enrollment = Enrollment.query.filter_by(enrollment_id=enrollment_id).first()
        if not enrollment:
            raise ValidationError(status_code=404, error_code="EVE1001", error_message="Enrollment not found")
        db.session.delete(enrollment)
        db.session.commit()
        return "", 204

class FeedbackAPI(Resource):
    @marshal_with(feedback_out_fields)
    @auth_required("token")
    @roles_required("Instructor")
    @roles_required("TA")
    def get(self, feed_id):
        feedback = Feedback.query.filter_by(feed_id=feed_id).first()
        if not feedback:
            raise ValidationError(status_code=404, error_code="FVE1001", error_message="Feedback not found")
        return feedback, 200

    @marshal_with(feedback_out_fields)
    @auth_required("token")
    @roles_required("Instructor")
    @roles_required("TA")
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
    @roles_required("Instructor")
    @roles_required("TA")
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
    @roles_required("Instructor")
    @roles_required("TA")
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
    @roles_required("Instructor")
    def get(self, kb_id):
        kb = KnowledgeBase.query.filter_by(kb_id=kb_id).first()
        if not kb:
            raise ValidationError(status_code=404, error_code="KVE1001", error_message="KnowledgeBase entry not found")
        return kb, 200

    @marshal_with(knowledgebase_out_fields)
    @auth_required("token")
    @roles_required("Instructor")
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
    @roles_required("Instructor")
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
    @roles_required("Instructor")
    def delete(self, kb_id):
        kb = KnowledgeBase.query.filter_by(kb_id=kb_id).first()
        if not kb:
            raise ValidationError(status_code=404, error_code="KVE1001", error_message="KnowledgeBase entry not found")
        db.session.delete(kb)
        db.session.commit()
        return "", 204


class GenAIConceptExplainerAPI(Resource):
    @auth_required("token")
    @roles_required("Student", "Instructor", "TA")
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
    @roles_required("Student", "Instructor")
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
    @roles_required("Student")
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

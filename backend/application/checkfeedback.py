from application.database import db
from application.models import User, Role, Course, Enrollment, SupplementaryContent, InstructorAlloted, Lecture, Assignment, QA, ProgQA, Scores, Queries, Feedback, KnowledgeBase
from application.validation import ValidationError

# Check if any feedback records exist
print(Feedback.query.all())  

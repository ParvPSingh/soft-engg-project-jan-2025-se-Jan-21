from main import app
from application.sec import datastore
from application.models import db
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name='Instructor', description='Instructor role found/created')
    datastore.find_or_create_role(name='TA', description='TA role found/created')
    datastore.find_or_create_role(name='Student', description='Student role found/created')
    db.session.commit()
    if not datastore.find_user(email='instructor@ds.study.iitm.ac.in'):
        datastore.create_user(
            name='Instructor', 
            email='instructor@ds.study.iitm.ac.in', 
            password=generate_password_hash('instruct', method="sha256"), 
            roles=['Instructor']
        )
    if not datastore.find_user(email='ta@ds.study.iitm.ac.in'):
        datastore.create_user(
            name='TA', 
            email='ta@ds.study.iitm.ac.in', 
            password=generate_password_hash('tata', method="sha256"), 
            roles=['TA']
        )
    db.session.commit()
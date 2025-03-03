from flask import Flask
from flask_cors import CORS
from application.models import db, User, Role
from application.resources import api
from config import DevelopmentConfig
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from application.sec import datastore

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    CORS(app, resources={r"/*":{'origins': "*"}})
    #CORS(app, resources={r"/*":{'origins': 'http://127.0.0.1:8080', "allow_headers":"Access-Control-Allow-Origin"}})
    db.init_app(app)
    api.init_app(app)
    app.security = Security(app, datastore=datastore)
    with app.app_context():
        import application.controllers
        db.create_all()
    return app

app = create_app()

if __name__=='__main__':
    
    app.run(debug=True)
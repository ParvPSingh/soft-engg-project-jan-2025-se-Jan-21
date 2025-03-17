from flask import Flask, request, jsonify
from flask_cors import CORS
from application.models import db, User, Role
from application.resources import api
from config import DevelopmentConfig
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from application.sec import datastore
from ta_chatbot import retrieve_context_ta, call_autobot_ta
from student_chatbot import retrieve_context_student, call_autobot_student

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
    
    #TA chatbot endpoint
    @app.route('/api/chatbot/ta', methods=['POST'])
    def ta_chatbot():
        data = request.get_json()
        user_query = data.get('message')
        retrieved_context = retrieve_context_ta(user_query)
        response = call_autobot_ta(user_query, retrieved_context)
        return jsonify({'response': response.content})
    
    #Student chatbot endpoint
    @app.route('/api/chatbot/student', methods=['POST'])
    def student_chatbot():
        data = request.get_json()
        user_query = data.get('message')
        retrieved_context = retrieve_context_student(user_query)
        response = call_autobot_student(user_query, retrieved_context)
        return jsonify({'response': response.content})

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
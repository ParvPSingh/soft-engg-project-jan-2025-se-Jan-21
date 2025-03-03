from flask import current_app as app, jsonify, request, render_template, send_file
from flask_security import auth_required, roles_required
from werkzeug.security import check_password_hash
from .sec import datastore
from application.models import User
from flask_restful import fields, marshal
from datetime import datetime, timedelta
from application.database import db
from collections import Counter
from sqlalchemy import and_

@app.get('/')
def home():
    return render_template("index.html")

@app.post('/login_user')
def user_login():
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
    
    if (user.active==False):
        return jsonify({"error_message": "You don't have access to the website"}), 401

    if check_password_hash(user.password, data.get("password")):
        return jsonify({"name": user.name, "token": user.get_auth_token(), "email": user.email, "role": user.roles[0].name, "user_id": user.user_id, "active": user.active})
    else:
        return jsonify({"error_message": "Wrong Password"}), 400
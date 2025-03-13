from flask import current_app as app, jsonify, request, render_template, send_file
from flask_security import auth_required, roles_required
from werkzeug.security import check_password_hash, generate_password_hash
from .sec import datastore
from application.models import User
from flask_restful import fields, marshal
from datetime import datetime, timedelta
from application.database import db
from collections import Counter
from sqlalchemy import and_
from flask import Flask, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from application.models import *


@app.get('/')
def home():
    return render_template("index.html")


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
    new_user = User(name=name, email=email, password=hashed_password, active=True, fs_uniquifier=email)

    # Assign default role 'Student'
    student_role = Role.query.filter_by(name="Student").first()
    if student_role:
        new_user.roles.append(student_role)

    db.session.add(new_user)
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
    
    if not user.active:
        return jsonify({"error_message": "You don't have access to the website"}), 401

    if check_password_hash(user.password, password):
        return jsonify({
            "name": user.name,
            "token": user.get_auth_token(),
            "email": user.email,
            "role": user.roles[0].name if user.roles else "User",  # ✅ Prevents IndexError
            "user_id": user.user_id,
            "active": user.active
        }), 200

    else:
        return jsonify({"error_message": "Wrong Password"}), 400

# Logout route
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200

@app.route('/api/user/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "id": user.user_id,
        "name": user.name,
        "email": user.email,
        "role": user.roles[0].name if user.roles else "User"
    })

@app.route('/api/user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user.name = data.get('name', user.name)
    if data.get('password'):
        user.password = generate_password_hash(data['password'], method="pbkdf2:sha256")

    db.session.commit()
    return jsonify({"message": "User updated successfully"})

@app.route('/api/user/<int:user_id>', methods=['DELETE'])
@roles_required('admin')
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

@app.route('/api/user/change-password', methods=['PUT'])
@login_required
def change_password():
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify({"error": "Old and new passwords are required"}), 400

    user = User.query.get(request.user_id)

    if not check_password_hash(user.password, old_password):
        return jsonify({"error": "Incorrect old password"}), 400

    user.password = generate_password_hash(new_password, method="pbkdf2:sha256")
    db.session.commit()

    return jsonify({"message": "Password changed successfully"}), 200

@app.route('/api/users', methods=['GET'])
@roles_required('admin')
def get_all_users():
    users = User.query.all()
    user_list = [{
        "id": user.user_id,
        "name": user.name,
        "email": user.email,
        "role": user.roles[0].name if user.roles else "User"
    } for user in users]

    return jsonify(user_list), 200

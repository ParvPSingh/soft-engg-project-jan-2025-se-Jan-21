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
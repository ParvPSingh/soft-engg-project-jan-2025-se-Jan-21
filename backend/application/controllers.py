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
    
    new_user = User(name=name, email=email, password=password, active=True, fs_uniquifier=email)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User created successfully"}), 201

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user or user.password != password:
        return jsonify({"error": "Invalid email or password"}), 401
    
    login_user(user)
    return jsonify({"message": "Login successful"}), 200

# Logout route
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200
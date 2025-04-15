from flask import Blueprint, request, jsonify
from backend.models.user import User
from backend.database import db
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(message="Username and password required"), 400

    if User.query.filter_by(username=username).first():
        return jsonify(message="Username already exists"), 409

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User registered successfully"), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=str(user.id))
        return jsonify(token=token), 200
    return jsonify(message='Invalid credentials'), 401

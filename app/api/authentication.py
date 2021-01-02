from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask import jsonify, request
from ..models import User
from . import api
from .errors import unauthorized, invalid_request


def verify_password(username, password):
    if username == '':
        return jsonify({"msg": "Invalid credentials"}), 400
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "Invalid credentials"}), 400
    if not user.verify_password(password):
        return jsonify({"msg": "Invalid credentials"}), 400
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@api.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    return verify_password(username, password)

@api.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
    





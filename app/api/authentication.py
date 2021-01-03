from flask_jwt_extended import create_access_token
from flask import jsonify, request
from ..models import User
from . import api


def verify_password(username, password):
    if username == "":
        return jsonify({"msg": "Invalid credentials"}), 400
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "Invalid credentials"}), 400
    if not user.verify_password(password):
        return jsonify({"msg": "Invalid credentials"}), 400
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@api.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    return verify_password(username, password)

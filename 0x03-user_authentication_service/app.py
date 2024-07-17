#!/usr/bin/env python3
"""
app module
"""

from flask import Flask, request, jsonify, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        return abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(400)

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

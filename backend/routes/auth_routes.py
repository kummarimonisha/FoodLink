from datetime import datetime, timedelta, timezone
from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

# Blueprint for all authentication-related routes.
# Registered in app.py with URL prefix: /api/auth
auth_bp = Blueprint("auth", __name__)


# ----------------------------------------------------------------------
# REGISTER — Create a new user account
# Endpoint: POST /api/auth/register
#
# Expected JSON body:
# {
#   "email": "example@mail.com",
#   "username": "user123",
#   "password": "mypassword",
#   "role": "donor"  // optional, defaults to "recipient"
# }
#
# Responses:
#   201 → user created successfully
#   400 → missing fields or email/username already exists
# ----------------------------------------------------------------------
@auth_bp.route("/register", methods=["POST"])
def auth_register():
    """
    User registration endpoint.
    Handles signup for donors, recipients, or admins (if needed).
    """
    data = request.get_json() or {}

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "recipient")

    if not email or not username or not password:
        return jsonify({"message": "Missing required fields"}), 400

    # Check if the email or username already exists.
    existing_user = User.query.filter(
        (User.email == email) | (User.username == username)
    ).first()

    if existing_user:
        return jsonify({"message": "Email or username already exists"}), 400

    # Create and persist the new user.
    user = User(
        email=email,
        username=username,
        role=role,
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# ----------------------------------------------------------------------
# LOGIN — Authenticate a user and return a JWT
# Endpoint: POST /api/auth/login
#
# JSON options:
# {
#   "email": "example@mail.com",
#   "password": "mypassword"
# }
#   OR
# {
#   "username": "user123",
#   "password": "mypassword"
# }
#
# Successful response:
# {
#   "message": "Login successful",
#   "access_token": "JWT_TOKEN_HERE",
#   "user": {
#       "id": ...,
#       "email": "...",
#       "username": "...",
#       "role": "donor" | "recipient" | "admin"
#   }
# }
#
# The frontend must store `access_token` and send it on protected routes
# using the Authorization header:
#   Authorization: Bearer <token>
# ----------------------------------------------------------------------
@auth_bp.route("/login", methods=["POST"])
def auth_login():
    """
    User login endpoint.
    Returns a JWT token if the credentials are valid.
    """
    data = request.get_json() or {}

    email_or_username = data.get("email") or data.get("username")
    password = data.get("password")

    if not email_or_username or not password:
        return jsonify({"message": "Missing credentials"}), 400

    # Find user by email or username.
    user = User.query.filter(
        (User.email == email_or_username) | (User.username == email_or_username)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    # JWT identity must be a string, so we store the user id as string.
    identity = str(user.id)

    # Additional claims can be included in the token payload if needed.
    additional_claims = {
        "role": user.role,
        "username": user.username,
    }

    # Generate the access token.
    access_token = create_access_token(
        identity=identity,
        additional_claims=additional_claims,
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role,
        },
    }), 200


# ----------------------------------------------------------------------
# ME — Get information about the currently authenticated user
# Endpoint: GET /api/auth/me
#
# Requires JWT:
#   Authorization: Bearer <token>
#
# Response:
# {
#   "message": "Current user",
#   "user_id": "3"
# }
#
# The frontend can use this endpoint to:
#   - verify if a token is still valid,
#   - detect the current logged-in user.
# ----------------------------------------------------------------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def auth_me():
    """
    Returns the user id stored in the current JWT identity.
    """
    current_user_id = get_jwt_identity()
    return jsonify({
        "message": "Current user",
        "user_id": current_user_id,
    }), 200


# ----------------------------------------------------------------------
# PING — Simple connectivity check for the auth blueprint
# Endpoint: GET /api/auth/ping
#
# Used to verify that the authentication routes are correctly registered.
# ----------------------------------------------------------------------
@auth_bp.route("/ping", methods=["GET"])
def auth_ping():
    """
    Simple endpoint to verify that the auth blueprint is registered.
    """
    return jsonify({"message": "auth blueprint is working"}), 200


# ----------------------------------------------------------------------
# FORGOT PASSWORD — Forgot a password
# Endpoint: POST /api/auth/forgot-password
#
# Expected JSON body:
# {
#   "email": "example@mail.com"
# }
#
# Responses:
#   201 → Created a reset password page
#   400 → missing email or user does not exist
# ----------------------------------------------------------------------
@auth_bp.route("/forgot-password", methods=["POST"])
def auth_forgot_password():
    data = request.get_json()

    email = data.get("email")

    if not email :
        return jsonify({"message": "Missing Email"}), 400

    # Check if the email or username already exists.
    existing_user = User.query.filter(
        (User.email == email)
    ).first()

    if not existing_user:
        return jsonify({"message": "User does not exist"}), 400

    token = generate_reset_token(email)

    new_password_url = f"http://localhost:3000/reset-password/{token}"

    return jsonify({"message": "The Reset Password Link has been sent to your email",
                    "reset_link": new_password_url}), 201

"""
Helper function for generating a token to reset a password that lasts 10 minutes.
"""
def generate_reset_token(email):
    payload = {
        "email": email,
        "type": "password_reset"
    }
    token = create_access_token(identity=email,
                                additional_claims=payload,
                                expires_delta=timedelta(minutes=10))
    return token


# ----------------------------------------------------------------------
# RESET PASSWORD — Reset a password
# Endpoint: POST /api/auth/reset-password
#
# Expected JSON body:
# {
#   "password": "mypassword"
# }
#
# JWT Headers:
# {
#   "email": "example@mail.com",
#   "type": "password_reset"
# }
# Responses:
#   200 → Password changed successfully
#   400 → missing token or password or user does not exist
# ----------------------------------------------------------------------
@auth_bp.route("/reset-password", methods=["POST"])
@jwt_required()
def auth_reset_password():
    """
    User registration endpoint.
    Handles signup for donors, recipients, or admins (if needed).
    """
    data = request.get_json()
    new_pass_info = get_jwt()
    email = new_pass_info.get("email")
    new_password = data.get("password")

    if not new_password :
        return jsonify({"message": "Missing New Password"}), 400


    if new_pass_info.get("type") != "password_reset":
        return jsonify({"message": "Invalid Token"}), 400
    
    # Check if the email or username already exists.
    existing_user = User.query.filter(
        (User.email == email)
    ).first()

    if not existing_user:
        return jsonify({"message": "User does not exist"}), 400

    existing_user.set_password(new_password)

    db.session.commit()

    return jsonify({"message": "Password Reset Successfully"}), 200

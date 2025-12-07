from datetime import timedelta

from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from email_utils import send_registration_email, send_password_reset_email
from security import role_required

# This blueprint groups all authentication-related routes
# and they will be prefixed with /api/auth in app.py
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def auth_register():
    """
    This endpoint is used to register a new user account.

    Steps:
    1. Validate requested data
    2. Check if user already exists
    3. Create the new user in the database
    4. Simulate sending a welcome email (printed in console)
    """
    data = request.get_json() or {}

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "recipient")  # default role if none is given

    if not email or not username or not password:
        return jsonify({"message": "Missing required fields"}), 400

    # Prevent duplicated accounts
    existing_user = User.query.filter(
        (User.email == email) | (User.username == username)
    ).first()
    if existing_user:
        return jsonify({"message": "Email or username already exists"}), 400

    # Save the new user
    user = User(email=email, username=username, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Email is only simulated for this project
    email_preview = send_registration_email(user.email, user.username)

    return jsonify({
        "message": "User registered successfully",
        "email_preview": email_preview,
    }), 201


@auth_bp.route("/login", methods=["POST"])
def auth_login():
    """
    Login endpoint.
    The user can log in using either their email or username.
    If the information is correct, we return a valid JWT token.
    """
    data = request.get_json() or {}
    email_or_username = data.get("email") or data.get("username")
    password = data.get("password")

    if not email_or_username or not password:
        return jsonify({"message": "Missing credentials"}), 400

    # Search for the user by email OR username
    user = User.query.filter(
        (User.email == email_or_username) | (User.username == email_or_username)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    if not user.is_active:
        return jsonify({"message": "Account is deactivated"}), 403

    # Create token that includes extra information for later use
    additional_claims = {
        "role": user.role,
        "username": user.username,
    }

    token = create_access_token(
        identity=str(user.id),
        additional_claims=additional_claims,
    )

    return jsonify({
        "message": "Login successful",
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role,
        },
    }), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def auth_me():
    """
    Get information about the currently logged-in user.
    Useful for session checks.
    """
    user_id = get_jwt_identity()
    claims = get_jwt()

    return jsonify({
        "message": "Current user",
        "user_id": user_id,
        "role": claims.get("role"),
        "username": claims.get("username"),
    }), 200


@auth_bp.route("/ping", methods=["GET"])
def auth_ping():
    """
    Very simple route to verify that the auth system is working correctly.
    """
    return jsonify({"message": "auth blueprint is working"}), 200


@auth_bp.route("/forgot-password", methods=["POST"])
def auth_forgot_password():
    """
    First step of password reset.

    What we do:
    - verify the email exists
    - generate a short-lived token (10 min)
    - simulate sending an email with a reset link
    """
    data = request.get_json() or {}
    email = data.get("email")

    if not email:
        return jsonify({"message": "Missing email"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        # In real systems we don't reveal this for security reasons
        return jsonify({"message": "User does not exist"}), 400

    token = generate_reset_token(email)
    reset_link = f"http://localhost:3000/reset-password/{token}"

    email_preview = send_password_reset_email(email, reset_link)

    return jsonify({
        "message": "Password reset link sent",
        "reset_link": reset_link,
        "email_preview": email_preview,
    }), 201


def generate_reset_token(email: str) -> str:
    """
    Generate a token for password reset.
    It expires in 10 minutes.
    """
    payload = {
        "email": email,
        "type": "password_reset",
    }

    return create_access_token(
        identity=email,
        additional_claims=payload,
        expires_delta=timedelta(minutes=10),
    )


@auth_bp.route("/reset-password", methods=["POST"])
@jwt_required()
def auth_reset_password():
    """
    Final step of resetting the password.
    The token must be valid and must be of the correct type.
    """
    data = request.get_json() or {}
    new_password = data.get("password")

    if not new_password:
        return jsonify({"message": "Missing new password"}), 400

    token_info = get_jwt()
    email = token_info.get("email")
    token_type = token_info.get("type")

    if token_type != "password_reset":
        return jsonify({"message": "Invalid token type"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User does not exist"}), 400

    user.set_password(new_password)
    db.session.commit()

    return jsonify({"message": "Password reset successfully"}), 200


@auth_bp.route("/profile/update", methods=["PATCH"])
@jwt_required()
def update_user():
    """
    This route allows logged users to change their username or email.
    """
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    new_username = data.get("username")
    new_email = data.get("email")

    if not new_username or not new_email:
        return jsonify({"msg": "Username and email required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 400

    # Validate that no other user has this username/email
    if User.query.filter(User.username == new_username, User.id != user_id).first():
        return jsonify({"msg": "Username already in use"}), 400

    if User.query.filter(User.email == new_email, User.id != user_id).first():
        return jsonify({"msg": "Email already in use"}), 400

    user.username = new_username
    user.email = new_email
    db.session.commit()

    return jsonify({
        "msg": "Profile updated",
        "user": {"username": user.username, "email": user.email},
    }), 200


@auth_bp.route("/admin/users", methods=["GET"])
@role_required(["admin"])
def admin_get_users():
    """
    Admin endpoint to list all users.
    Returns user id, username, email, and role.
    """
    users = User.query.all()
    user_list = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
        }
        for user in users
    ]
    return jsonify(user_list), 200


@auth_bp.route("/admin/users/<int:user_id>/deactivate", methods=["PATCH"])
@role_required(["admin"])  # only admins can deactivate users
def admin_deactivate_user(user_id: int):
    """
    Used by admins to deactivate a user.
    A deactivated user cannot log in.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_active = False
    db.session.commit()

    return jsonify({"message": "User deactivated successfully"}), 200


@auth_bp.route("/admin/users/<int:user_id>/activate", methods=["PATCH"])
@role_required(["admin"])
def admin_activate_user(user_id: int):
    """
    Reactivate a previously deactivated user (admin only).
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_active = True
    db.session.commit()

    return jsonify({"message": "User activated successfully"}), 200

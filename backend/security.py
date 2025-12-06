from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import User


def role_required(allowed_roles):
    """
    Custom decorator used to protect routes by user roles.
    It ensures that the logged-in user has one of the allowed roles.

    Usage examples:
        @role_required(["admin"])
        def only_admin_route():
            ...

        @role_required(["donor", "admin"])
        def donor_or_admin_route():
            ...
    """

    def decorator(fn):
        @wraps(fn)
        @jwt_required()  # Ensures the request includes a valid JWT token
        def wrapper(*args, **kwargs):
            # Extracts the user ID stored in the JWT token
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            # If the token refers to a missing user in DB → reject
            if user is None:
                return jsonify({"message": "User not found"}), 404

            # If the user has been deactivated by an admin → reject
            if not user.is_active:
                return jsonify({"message": "User is deactivated"}), 403

            # Check if role is allowed to access this route
            if user.role not in allowed_roles:
                return jsonify({"message": "Insufficient permissions"}), 403

            # If all checks pass → run original view function
            return fn(*args, **kwargs)

        return wrapper

    return decorator

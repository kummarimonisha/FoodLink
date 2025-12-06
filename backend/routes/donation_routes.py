from flask import Blueprint, request, jsonify
from models import db, Donation
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt
from functools import wraps

# Blueprint for donation-related routes.
# Registered in app.py with URL prefix: /api/donations
donation_bp = Blueprint("donations", __name__)


# ----------------------------------------------------------------------
# CREATE DONATION
# Endpoint: POST /api/donations/
#
# PROTECTED route → requires JWT token
# Header:
#   Authorization: Bearer <token>
#
# Expected JSON body:
# {
#   "title": "Food box",
#   "description": "Includes rice and beans",
#   "category": "non_perishable",
#   "quantity": 4
# }
#
# Notes:
# - donor_id is NOT sent from the frontend.
# - donor_id is inferred from the JWT identity (logged-in user).
#
# Responses:
#   201 → donation created successfully
#   400 → missing fields or invalid data
# ----------------------------------------------------------------------
@donation_bp.route("/", methods=["POST"])
@jwt_required()
def create_donation():
    """
    Create a new donation. Only authenticated users can create donations.
    The donor id is taken from the JWT identity, not from the request body.
    """
    data = request.get_json() or {}

    title = data.get("title")
    description = data.get("description")
    category = data.get("category")
    quantity = data.get("quantity")

    if not title or not quantity:
        return jsonify({"message": "Missing required fields"}), 400

    # Ensure quantity is numeric.
    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({"message": "Quantity must be a number"}), 400

    # Get user id from JWT identity.
    current_user_id = get_jwt_identity()
    try:
        donor_id = int(current_user_id)
    except (TypeError, ValueError):
        return jsonify({"message": "Invalid user id in token"}), 400

    donation = Donation(
        title=title,
        description=description,
        category=category,
        quantity=quantity,
        expiration_date=None,
        donor_id=donor_id,
        status="pending",
    )

    db.session.add(donation)
    db.session.commit()

    return jsonify({
        "message": "Donation created successfully",
        "donation": {
            "id": donation.id,
            "title": donation.title,
            "quantity": donation.quantity,
            "status": donation.status,
        },
    }), 201


# ----------------------------------------------------------------------
# LIST AVAILABLE DONATIONS
# Endpoint: GET /api/donations/available
#
# PUBLIC route → does not require authentication.
# The frontend can use this to show all donations that are not rejected.
#
# Response (example):
# [
#   {
#     "id": 1,
#     "title": "Canned food",
#     "description": "4 canned items",
#     "category": "non_perishable",
#     "quantity": 4,
#     "status": "pending",
#     "donor_id": 2
#   },
#   ...
# ]
# ----------------------------------------------------------------------
@donation_bp.route("/available", methods=["GET"])
def get_available_donations():
    """
    List all donations that are not rejected.
    This endpoint is public.
    """
    donations = Donation.query.filter(Donation.status== "approved").all()
    #CHANGED FROM NOT REJECTED TO ONLY APPROVED
    result = []
    for d in donations:
        result.append({
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "category": d.category,
            "quantity": d.quantity,
            "status": d.status,
            "donor_id": d.donor_id,
        })

    return jsonify(result), 200


# ----------------------------------------------------------------------
# LIST MY DONATIONS
# Endpoint: GET /api/donations/mine
#
# PROTECTED route → requires JWT token
# Header:
#   Authorization: Bearer <token>
#
# Returns all donations created by the currently logged-in user.
#
# Response (example):
# [
#   {
#     "id": 1,
#     "title": "Food box",
#     "description": "Includes rice and beans",
#     "category": "non_perishable",
#     "quantity": 4,
#     "status": "pending"
#   },
#   ...
# ]
# ----------------------------------------------------------------------
@donation_bp.route("/mine", methods=["GET"])
@jwt_required()
def get_my_donations():
    """
    List all donations belonging to the currently authenticated user.
    """
    current_user_id = get_jwt_identity()
    try:
        donor_id = int(current_user_id)
    except (TypeError, ValueError):
        return jsonify({"message": "Invalid user id in token"}), 400

    donations = Donation.query.filter_by(donor_id=donor_id).all()

    result = []
    for d in donations:
        result.append({
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "category": d.category,
            "quantity": d.quantity,
            "status": d.status,
        })

    return jsonify(result), 200


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request() 
        claims = get_jwt()

        if claims.get("role") != "admin":
            return jsonify(msg="Admins only"), 403
        
        return fn(*args, **kwargs)

    return wrapper

# ----------------------------------------------------------------------
# LIST PENDING DONATIONS
# Endpoint: GET /api/donations/admin/pending
#
# PROTECTED route → requires JWT token
# ADMIN route → requires admin role
# Header:
#   Authorization: Bearer <token>
#
# Returns all donations that are pending.
#
# Response (example):
# [
#   {
#     "id": 1,
#     "title": "Food box",
#     "description": "Includes rice and beans",
#     "category": "non_perishable",
#     "quantity": 4,
#     "status": "pending"
#   },
#   ...
# ]
# ----------------------------------------------------------------------
@donation_bp.route("/admin/pending", methods=["GET"])
@jwt_required()
@admin_required
def get_pending_donations():
    """
    List all donations belonging to the currently authenticated user.
    """
    current_user_id = get_jwt_identity()

    donations = Donation.query.filter_by(status="pending").all()

    result = []
    for d in donations:
        result.append({
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "category": d.category,
            "quantity": d.quantity,
            "status": d.status,
        })

    return jsonify(result), 200

# ----------------------------------------------------------------------
# ACCEPT DONATION
# Endpoint: GET /api/donations/admin/donation.id/approve
#
# PROTECTED route → requires JWT token
# ADMIN route → requires admin role
# Header:
#   Authorization: Bearer <token>
#
# Approves donation
# ----------------------------------------------------------------------
@donation_bp.route("/admin/<int:donation_id>/approve", methods=["PATCH"])
@jwt_required()
@admin_required
def approve_donation(donation_id):
    """
    List all donations belonging to the currently authenticated user.
    """
    donation = Donation.query.get_or_404(donation_id)
    donation.status = "approved"
    db.session.commit()
    return jsonify({"message": "Donation Approved"}), 200

# ----------------------------------------------------------------------
# ACCEPT DONATION
# Endpoint: GET /api/donations/admin/donation.id/reject
#
# PROTECTED route → requires JWT token
# ADMIN route → requires admin role
# Header:
#   Authorization: Bearer <token>
#
# Rejects donation
# ----------------------------------------------------------------------
@donation_bp.route("/admin/<int:donation_id>/reject", methods=["PATCH"])
@jwt_required()
@admin_required
def reject_donation(donation_id):
    """
    List all donations belonging to the currently authenticated user.
    """
    donation = Donation.query.get_or_404(donation_id)
    donation.status = "rejected"
    db.session.commit()
    return jsonify({"message": "Donation rejected"}), 200
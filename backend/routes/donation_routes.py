from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from models import db, User, Donation

# This blueprint groups all donation-related API routes.
# The prefix /api/donations is applied in app.py
donation_bp = Blueprint("donations", __name__)


# ----------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------

def get_current_user():
    """
    Extract the currently logged-in user using the JWT token.
    The token stores the user ID as the identity.
    """
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return User.query.get(user_id)


def require_role(user, allowed_roles):
    """
    Small permission helper.
    Checks that the user:
    - exists
    - is active
    - has a role in the allowed list

    Returns True if the user is allowed to continue,
    otherwise returns False.
    """
    if user is None:
        return False
    if not user.is_active:
        return False
    if user.role not in allowed_roles:
        return False
    return True


# ----------------------------------------------------------
# 1) Create a donation  (Only donors)
#    POST /api/donations/
# ----------------------------------------------------------
@donation_bp.post("/")
@jwt_required()
def create_donation():
    """
    Donors create new donations.
    The donation starts with status = "pending"
    and must be approved by an admin.
    """
    user = get_current_user()
    if not require_role(user, ["donor"]):
        return jsonify({"message": "Only donors can create donations"}), 403

    data = request.get_json() or {}

    title = data.get("title")
    quantity = data.get("quantity")
    description = data.get("description")
    category = data.get("category")
    expiration_date_str = data.get("expiration_date")

    if not title or quantity is None:
        return jsonify({"message": "title and quantity are required"}), 400

    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({"message": "quantity must be an integer"}), 400

    # Convert expiration date string (ISO format) into a Python datetime
    expiration_date = None
    if expiration_date_str:
        try:
            expiration_date = datetime.fromisoformat(expiration_date_str)
        except ValueError:
            return jsonify({"message": "Invalid expiration_date format"}), 400

    donation = Donation(
        title=title,
        description=description,
        category=category,
        quantity=quantity,
        expiration_date=expiration_date,
        status="pending",
        donor_id=user.id,
    )

    db.session.add(donation)
    db.session.commit()

    return jsonify({
        "message": "Donation created and pending approval",
        "donation": {
            "id": donation.id,
            "title": donation.title,
            "quantity": donation.quantity,
            "status": donation.status,
        },
    }), 201


# ----------------------------------------------------------
# 2) List available donations (approved + not expired)
#    GET /api/donations/available
# ----------------------------------------------------------
@donation_bp.get("/available")
@jwt_required()
def get_available_donations():
    """
    Recipients can browse the available donations.

    Filters applied:
    - status must be "approved"
    - not expired (based on expiration_date)
    """
    user = get_current_user()
    if not require_role(user, ["recipient", "donor", "admin"]):
        return jsonify({"message": "Not authorized"}), 403

    now = datetime.utcnow()

    donations = Donation.query.filter(
        Donation.status == "approved",
        (Donation.expiration_date.is_(None) | (Donation.expiration_date > now)),
    ).order_by(Donation.created_at.desc()).all()

    result = []
    for d in donations:
        result.append({
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "category": d.category,
            "quantity": d.quantity,
            "status": d.status,
            "expiration_date": d.expiration_date.isoformat() if d.expiration_date else None,
            "donor_id": d.donor_id,
        })

    return jsonify(result), 200


# ----------------------------------------------------------
# 3) Admin view: see pending donations
#    GET /api/donations/pending
# ----------------------------------------------------------
@donation_bp.get("/pending")
@jwt_required()
def get_pending_donations():
    """
    Admins can view all donations waiting for approval.
    """
    user = get_current_user()
    if not require_role(user, ["admin"]):
        return jsonify({"message": "Admin only"}), 403

    donations = Donation.query.filter_by(status="pending").order_by(
        Donation.created_at.desc()
    ).all()

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


# ----------------------------------------------------------
# 4) Admin: Reject donation
#    POST /api/donations/<id>/reject
# ----------------------------------------------------------
@donation_bp.post("/<int:donation_id>/reject")
@jwt_required()
def reject_donation(donation_id):
    """
    Admins can reject a donation if it is still pending.
    """
    user = get_current_user()
    if not require_role(user, ["admin"]):
        return jsonify({"message": "Admin only"}), 403

    donation = Donation.query.get_or_404(donation_id)

    if donation.status in ["allocated", "expired", "rejected"]:
        return jsonify({"message": "Cannot reject in current status"}), 400

    donation.status = "rejected"
    db.session.commit()

    return jsonify({"message": "Donation rejected", "donation_id": donation.id}), 200


# ----------------------------------------------------------
# 5) Recipient: Claim donation
#    POST /api/donations/<id>/claim
# ----------------------------------------------------------
@donation_bp.post("/<int:donation_id>/claim")
@jwt_required()
def claim_donation(donation_id):
    """
    A recipient tries to claim a donation.

    Conditions checked:
    - donation not expired
    - must be approved and not already claimed
    - first requester gets it (like a race)
    """
    user = get_current_user()
    if not require_role(user, ["recipient"]):
        return jsonify({"message": "Only recipients can claim donations"}), 403

    donation = Donation.query.get_or_404(donation_id)

    if donation.is_expired:
        donation.status = "expired"
        db.session.commit()
        return jsonify({"message": "Donation expired"}), 400

    # Ensure donation is still available (approved and not claimed)
    if donation.status != "approved" or donation.allocated_to_id is not None:
        return jsonify({"message": "Donation is not available for claiming"}), 400

    donation.status = "allocated"
    donation.allocated_to_id = user.id
    db.session.commit()

    return jsonify({
        "message": "Donation allocated successfully",
        "donation_id": donation.id,
        "allocated_to": user.id,
    }), 200


# ----------------------------------------------------------
# 6) Admin: Deactivate a user
#    POST /api/donations/admin/users/<user_id>/deactivate
# ----------------------------------------------------------
@donation_bp.post("/admin/users/<int:user_id>/deactivate")
@jwt_required()
def deactivate_user(user_id):
    """
    Admin can deactivate users who break the rules.
    When deactivated, the user can no longer log in.
    """
    admin = get_current_user()
    if not require_role(admin, ["admin"]):
        return jsonify({"message": "Admin only"}), 403

    user = User.query.get_or_404(user_id)

    if not user.is_active:
        return jsonify({"message": "User already deactivated"}), 400

    user.is_active = False
    db.session.commit()

    return jsonify({"message": "User deactivated", "user_id": user.id}), 200


# ----------------------------------------------------------
# 7) Admin: Approve donation
#    POST /api/donations/<id>/approve
# ----------------------------------------------------------
@donation_bp.post("/<int:donation_id>/approve")
@jwt_required()
def approve_donation(donation_id):
    """
    Admin approves a pending donation.
    If the expiration date already passed, we mark it expired instead.
    """
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if not require_role(admin, ["admin"]):
        return jsonify({"message": "Admin only"}), 403

    donation = Donation.query.get_or_404(donation_id)

    if donation.status != "pending":
        return jsonify({"message": "Donation is not pending"}), 400

    if donation.expiration_date and donation.expiration_date < datetime.utcnow():
        donation.status = "expired"
        db.session.commit()
        return jsonify({"message": "Donation already expired"}), 400

    donation.status = "approved"
    db.session.commit()

    return jsonify({
        "message": "Donation approved",
        "donation_id": donation.id
    }), 200

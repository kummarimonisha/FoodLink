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
# 2) Edit a donation (Only donor owner or admin)
#    PATCH /api/donations/<id>
# ----------------------------------------------------------
@donation_bp.patch("/<int:donation_id>")
@jwt_required()
def update_donation(donation_id):
    """
    Edit an existing donation.

    Rules:
    - Only the original donor or an admin can edit a donation.
    - Only donations in 'pending' status can be edited.
    - Fields are optional; only provided fields will be updated.
    """
    current_user = get_current_user()
    if not require_role(current_user, ["donor", "admin"]):
        return jsonify({"message": "Only donors or admins can edit donations"}), 403

    donation = Donation.query.get_or_404(donation_id)

    # Only the donor who created it OR an admin can edit
    if current_user.role != "admin" and donation.donor_id != current_user.id:
        return jsonify({"message": "You are not allowed to edit this donation"}), 403

    # Do not allow editing if the donation is no longer pending
    if donation.status != "pending":
        return jsonify({"message": "Only pending donations can be edited"}), 400

    data = request.get_json() or {}

    title = data.get("title")
    description = data.get("description")
    category = data.get("category")
    quantity = data.get("quantity")
    expiration_date_str = data.get("expiration_date")

    # Optional updates: only override if a field is present in the request
    if title is not None:
        donation.title = title

    if description is not None:
        donation.description = description

    if category is not None:
        donation.category = category

    if quantity is not None:
        try:
            donation.quantity = int(quantity)
        except ValueError:
            return jsonify({"message": "quantity must be an integer"}), 400

    if expiration_date_str is not None:
        if expiration_date_str == "":
            # Allow clearing expiration date if empty string is sent
            donation.expiration_date = None
        else:
            try:
                donation.expiration_date = datetime.fromisoformat(expiration_date_str)
            except ValueError:
                return jsonify({"message": "Invalid expiration_date format (use ISO)"}), 400

    db.session.commit()

    return jsonify(
        {
            "message": "Donation updated successfully",
            "donation": {
                "id": donation.id,
                "title": donation.title,
                "description": donation.description,
                "category": donation.category,
                "quantity": donation.quantity,
                "status": donation.status,
                "expiration_date": donation.expiration_date.isoformat()
                if donation.expiration_date
                else None,
                "donor_id": donation.donor_id,
            },
        }
    ), 200


# ----------------------------------------------------------
# 3) List available donations (approved + not expired)
#    GET /api/donations/available
# ----------------------------------------------------------
@donation_bp.get("/available")
@jwt_required()
def get_available_donations():
    """
    List approved and non-expired donations.

    This endpoint now also supports basic filtering by category,
    which is similar to the FoodItem "type" in the class diagram.

    Query params:
      - category=fruit
      - category=fruit&category=vegetable
      - category=fruit,vegetable
    """
    user = get_current_user()
    if not require_role(user, ["recipient", "donor", "admin"]):
        return jsonify({"message": "Not authorized"}), 403

    now = datetime.utcnow()

    # Base query: only approved and not expired donations
    query = Donation.query.filter(
        Donation.status == "approved",
        (Donation.expiration_date.is_(None) | (Donation.expiration_date > now)),
    )

    # ------------------------------------------------------------------
    # Optional filters
    # ------------------------------------------------------------------
    # We use the "category" field of Donation to approximate FoodItem.type
    # from the class diagram.
    #
    # Examples:
    #   /api/donations/available?category=fruit
    #   /api/donations/available?category=fruit&category=vegetable
    #   /api/donations/available?category=fruit,vegetable
    categories = request.args.getlist("category")

    # If the frontend sends a single comma-separated string, handle it too
    if not categories:
        single_category = request.args.get("category")
        if single_category:
            categories = [
                c.strip() for c in single_category.split(",") if c.strip()
            ]

    if categories:
        query = query.filter(Donation.category.in_(categories))

    # Execute the final query
    donations = query.order_by(Donation.created_at.desc()).all()

    result = []
    for d in donations:
        result.append(
            {
                "id": d.id,
                "title": d.title,
                "description": d.description,
                "category": d.category,
                "quantity": d.quantity,
                "status": d.status,
                "expiration_date": d.expiration_date.isoformat()
                if d.expiration_date
                else None,
                "donor_id": d.donor_id,
            }
        )

    return jsonify(result), 200

# ----------------------------------------------------------
# 4) Admin view: see pending donations
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
# 5) Admin: Reject donation
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
# 6) Recipient: Claim donation
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

    # 1) Check for expiration
    if donation.is_expired:
        donation.status = "expired"
        db.session.commit()
        return jsonify({"message": "Donation expired"}), 400

    # 2) Ensure donation is still available (approved and not claimed)
    if donation.status != "approved" or donation.allocated_to_id is not None:
        return jsonify({"message": "Donation is not available for claiming"}), 400

    # 3) Allocate to the first recipient that arrives
    donation.status = "allocated"
    donation.allocated_to_id = user.id
    db.session.commit()

    return jsonify({
        "message": "Donation allocated successfully",
        "donation_id": donation.id,
        "allocated_to": user.id,
    }), 200


# ----------------------------------------------------------
# 7) Admin: Deactivate a user
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
# 8) Admin: Approve donation
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

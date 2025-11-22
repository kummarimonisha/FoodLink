from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Global SQLAlchemy instance used to define models and interact with the DB.
db = SQLAlchemy()


# ---------------------------------------------------------------------
# MODEL: User
# Represents each user in the FoodLink system.
# Possible roles:
#   - "donor"      (donates food)
#   - "recipient"  (receives food)
#   - "admin"      (optional, can manage/approve donations)
# ---------------------------------------------------------------------
class User(db.Model):
    __tablename__ = "users"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Unique email address used for login or contact.
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Unique username used for login and display.
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Hashed password (never store plain text passwords).
    password_hash = db.Column(db.String(255), nullable=False)

    # User role in the system.
    role = db.Column(db.String(20), nullable=False, default="recipient")

    # Whether the account is active (for future account suspension logic).
    is_active = db.Column(db.Boolean, default=True)

    # Timestamp when the user was created.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ------------------------------
    # Password utilities
    # ------------------------------

    def set_password(self, password: str) -> None:
        """
        Hash and store the given plain text password.
        Used during registration or when resetting passwords.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verify a plain text password against the stored hash.
        Used during login.
        """
        return check_password_hash(self.password_hash, password)


# ---------------------------------------------------------------------
# MODEL: Donation
# Represents a donation created by a user with role "donor".
#
# The frontend will use this model for:
#   - Creating new donations
#   - Listing available donations
#   - Showing a donor their own donations
# ---------------------------------------------------------------------
class Donation(db.Model):
    __tablename__ = "donations"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Short title describing the donation (required).
    title = db.Column(db.String(120), nullable=False)

    # Optional detailed description.
    description = db.Column(db.Text, nullable=True)

    # Optional category, e.g.: "non_perishable", "prepared_food", etc.
    category = db.Column(db.String(50), nullable=True)

    # Quantity or number of units/items donated.
    quantity = db.Column(db.Integer, nullable=False)

    # Optional expiration date (for perishable food).
    expiration_date = db.Column(db.DateTime, nullable=True)

    # Donation status:
    #   "pending"   → just created
    #   "approved"  → approved by admin (optional flow)
    #   "allocated" → assigned/delivered to a recipient
    #   "rejected"  → rejected by admin
    status = db.Column(db.String(20), default="pending")

    # Timestamp when the donation was created.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key relationship to the donor (User model).
    donor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relationship to the User object.
    # donation.donor → User instance
    # user.donations → list of Donation instances
    donor = db.relationship("User", backref="donations")

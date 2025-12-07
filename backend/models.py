from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

# Global SQLAlchemy database object used across the whole application
db = SQLAlchemy()


# ---------------------------------------------------------------
# USER MODEL
# This table stores every user in FoodLink.
#
# Roles:
#   - donor: can create food donations
#   - recipient: can claim available donations
#   - admin: has permission to approve/reject donations and
#            deactivate users if needed
# ---------------------------------------------------------------
class User(db.Model):
    __tablename__ = "users"

    # Primary key (unique id automatically generated)
    id = db.Column(db.Integer, primary_key=True)

    # Email must be unique because it is used for login.
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Username also must be unique (used for identification in UI).
    username = db.Column(db.String(80), unique=True, nullable=False)

    # This is the hashed version of the password.
    # We should NEVER store raw passwords in a database.
    password_hash = db.Column(db.String(255), nullable=False)

    # Defines the type of user in the system.
    role = db.Column(db.String(20), nullable=False, default="recipient")

    # If false → user cannot log in or interact in the system.
    is_active = db.Column(db.Boolean, default=True)

    # When the user account was created (stored automatically).
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # ------------------------------
    # Password helpers
    # ------------------------------

    def set_password(self, password: str) -> None:
        """
        Takes a raw password and saves only a secure hashed version of it.
        Used during registration or when changing password.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Checks if the provided password matches the stored hash.
        Used during login authentication.
        """
        return check_password_hash(self.password_hash, password)


# ---------------------------------------------------------------
# DONATION MODEL
# Each donation is created by a donor user.
#
# Main purposes:
#   - Store donation items shared by donors
#   - Display available donations to recipients
#   - Track allocation when a recipient claims a donation
# ---------------------------------------------------------------
class Donation(db.Model):
    __tablename__ = "donations"

    id = db.Column(db.Integer, primary_key=True)

    # Short name of the donation item (ex: “Bread Loaf”)
    title = db.Column(db.String(120), nullable=False)

    # Optional extra details describing the donation
    description = db.Column(db.Text, nullable=True)

    # Simple category (could be used for filtering later)
    category = db.Column(db.String(50), nullable=True)

    # Quantity of items/units available
    quantity = db.Column(db.Integer, nullable=False)

    # For perishable food items — helps the system mark expired donations
    expiration_date = db.Column(db.DateTime, nullable=True)

    # Status used to track approval / allocation workflow
    status = db.Column(db.String(20), default="pending")

    # Timestamp when the donation was first created
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Link to the donor user that created this donation
    donor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    donor = db.relationship(
        "User", foreign_keys=[donor_id], backref="donations"
    )

    # Optional: if a recipient claims the donation
    allocated_to_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    allocated_to = db.relationship("User", foreign_keys=[allocated_to_id])

    @property
    def is_expired(self) -> bool:
        """
        Helper that checks if the donation should be considered expired.
        If it has an expiration date and that date has already passed,
        the donation is no longer valid for claiming.
        """
        return (
            self.expiration_date is not None
            and self.expiration_date < datetime.now(timezone.utc)
        )
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db, User
from routes.auth_routes import auth_bp
from routes.donation_routes import donation_bp
from flask_jwt_extended import JWTManager


# Global JWT manager instance used across the application.
jwt = JWTManager()


def create_app():
    """
    Application factory function.
    Initializes Flask, database, JWT, CORS and registers blueprints.
    All backend API endpoints are exposed from here.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS so the frontend (e.g., React) can call the API.
    CORS(app)

    # Initialize database and JWT with this app instance.
    db.init_app(app)
    jwt.init_app(app)

    # Create database tables if they do not exist (development convenience).
    with app.app_context():
        db.create_all()

    # ------------------------------------------------------------------
    # Internal test/utility endpoints (not intended for production use)
    # ------------------------------------------------------------------

    @app.route("/api/health", methods=["GET"])
    def health_check():
        """
        Simple health check endpoint.
        The frontend can call this to verify that the backend is running.
        """
        return jsonify({"status": "ok", "message": "FoodLink backend is running"}), 200

    @app.route("/api/create-test-user", methods=["GET"])
    def create_test_user():
        """
        Utility endpoint to create a sample user for testing.
        NOT intended for production. Used only during development.
        """
        existing = User.query.filter_by(email="test@example.com").first()
        if existing:
            return jsonify({"message": "Test user already exists"}), 200

        user = User(
            email="test@example.com",
            username="testuser",
            role="donor",
        )
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Test user created"}), 201

    # ------------------------------------------------------------------
    # Blueprint registration
    # ------------------------------------------------------------------

    # Authentication endpoints: /api/auth/...
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # Donation endpoints: /api/donations/...
    app.register_blueprint(donation_bp, url_prefix="/api/donations")

    return app


# Entry point for running the app locally with `python app.py`
if __name__ == "__main__":
    app = create_app()
    # debug=True enables auto-reload and detailed error pages during development.
    app.run(debug=True)

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db, User
from routes.auth_routes import auth_bp
from routes.donation_routes import donation_bp
from flask_jwt_extended import JWTManager

# Global JWT manager instance used by the whole application
jwt = JWTManager()


def create_app():
    """
    App factory function.

    - Creates the Flask app instance
    - Loads configuration
    - Initializes database, CORS and JWT
    - Registers the main blueprints (auth, donations)
    """
    app = Flask(__name__)

    # Load configuration from the Config class (config.py)
    app.config.from_object(Config)

    # Allow requests from the frontend (for example, React on another port)
    CORS(app)

    # Attach the database and JWT manager to this app instance
    db.init_app(app)
    jwt.init_app(app)

    # Create database tables if they don't exist yet
    # (this is mainly for development convenience)
    with app.app_context():
        db.create_all()

    # ------------------------------------------------------------------
    # Simple internal / utility routes
    # ------------------------------------------------------------------

    @app.route("/api/health", methods=["GET"])
    def health_check():
        """
        Health check endpoint.
        The frontend can call this to confirm the backend is up.
        """
        return jsonify({
            "status": "ok",
            "message": "FoodLink backend is running",
        }), 200

    @app.route("/api/create-test-user", methods=["GET"])
    def create_test_user():
        """
        Creates a test user in the database.
        This is only for local testing, not for production use.
        """
        # Check if the test user already exists
        existing = User.query.filter_by(email="test@example.com").first()
        if existing:
            return jsonify({"message": "Test user already exists"}), 200

        # Create a new donor user
        user = User(
            email="test@example.com",
            username="testuser",
            role="donor",
        )

        # Save the password hashed using the model's helper method
        user.set_password("password123")

        # Add and commit the new user to the database
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Test user created"}), 201

    # ------------------------------------------------------------------
    # Blueprint registration
    # ------------------------------------------------------------------

    # All auth-related routes will start with /api/auth/...
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # All donation-related routes will start with /api/donations/...
    app.register_blueprint(donation_bp, url_prefix="/api/donations")

    return app


# Entry point when running:  python app.py
if __name__ == "__main__":
    app = create_app()
    # debug=True auto-reloads the server and shows detailed errors (dev only)
    app.run(debug=True)
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db, User
from routes.auth_routes import auth_bp
from routes.donation_routes import donation_bp
from flask_jwt_extended import JWTManager


jwt = JWTManager()

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    # Crear las tablas en foodlink.db
    with app.app_context():
        db.create_all()

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok", "message": "FoodLink backend is running"}), 200

    @app.route("/api/create-test-user", methods=["GET"])
    def create_test_user():
        existing = User.query.filter_by(email="test@example.com").first()
        if existing:
            return jsonify({"message": "Test user already exists"}), 200

        user = User(
            email="test@example.com",
            username="testuser",
            role="donor"
        )
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Test user created"}), 201

    # 👇 MUY IMPORTANTE: esto va FUERA de la función create_test_user
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(donation_bp, url_prefix="/api/donations")

    return app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

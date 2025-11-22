from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db, User
from routes.auth_routes import auth_bp
from routes.donation_routes import donation_bp
from flask_jwt_extended import JWTManager


# Inicializo la extensión JWT a nivel global.
# El frontend usará los tokens generados aquí para autenticación.
jwt = JWTManager()


def create_app():
    """
    Esta función crea y configura la aplicación Flask.
    Aquí inicializo la BD, JWT, CORS y registro los blueprints.
    El frontend consumirá todos los endpoints que se exponen
    bajo /api/auth y /api/donations.
    """

    # Creo la instancia de Flask
    app = Flask(__name__)

    # Cargo la configuración desde config.py (Base de datos, JWT_KEY, etc.)
    app.config.from_object(Config)

    # Habilito CORS para permitir requests desde el frontend (React o el que sea)
    CORS(app)

    # Inicializo SQLAlchemy y JWT dentro de la app
    db.init_app(app)
    jwt.init_app(app)

    # Creo las tablas automáticamente si no existen
    # Esto solo corre en ambiente local, útil para desarrollo
    with app.app_context():
        db.create_all()

    # ------------ RUTAS INTERNAS DE PRUEBA (NO SE USAN EN PRODUCCIÓN) ------------

    @app.route("/api/health", methods=["GET"])
    def health_check():
        """
        Ruta simple para verificar que el backend está levantado.
        El frontend puede usarla para un "ping" inicial.
        """
        return jsonify({"status": "ok", "message": "FoodLink backend is running"}), 200

    @app.route("/api/create-test-user", methods=["GET"])
    def create_test_user():
        """
        Ruta SOLO PARA PRUEBAS.
        Crea un usuario inicial con email test@example.com.
        Esto ayuda en desarrollo cuando todavía no existe un frontend.
        """
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

    # ------------ BLUEPRINTS CON LAS RUTAS DEL BACKEND ------------

    # Rutas de autenticación: register, login, me
    # URL base: /api/auth/...
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # Rutas de donaciones: crear donación, listar, ver mis donaciones, etc.
    # URL base: /api/donations/...
    app.register_blueprint(donation_bp, url_prefix="/api/donations")

    return app


# Punto de entrada cuando se ejecuta python app.py
if __name__ == "__main__":
    app = create_app()

    # debug=True para recargar automáticamente cambios durante desarrollo
    app.run(debug=True)

from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

# Blueprint específico para autenticación.
# El prefix es /api/auth (registrado en app.py)
auth_bp = Blueprint("auth", __name__)


# ----------------------------------------------------------------------
# REGISTER — Crear nuevo usuario
# Endpoint: POST /api/auth/register
#
# El frontend debe enviar un JSON con:
# {
#   "email": "example@mail.com",
#   "username": "user123",
#   "password": "mypassword",
#   "role": "donor"  (opcional, por defecto "recipient")
# }
#
# Respuestas:
#   201 → usuario creado correctamente
#   400 → faltan campos o email/username ya usados
# ----------------------------------------------------------------------
@auth_bp.route("/register", methods=["POST"])
def auth_register():
    """
    Register a new user.
    Handles signup for donors, recipients, or admin (if needed).
    """
    data = request.get_json() or {}

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "recipient")  # default role

    # Validación de campos requeridos
    if not email or not username or not password:
        return jsonify({"message": "Missing required fields"}), 400

    # Verificar si email o username ya existen
    existing_user = User.query.filter(
        (User.email == email) | (User.username == username)
    ).first()

    if existing_user:
        return jsonify({"message": "Email or username already exists"}), 400

    # Crear nuevo usuario
    user = User(
        email=email,
        username=username,
        role=role,
    )
    user.set_password(password)  # Guardar hash seguro

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201



# ----------------------------------------------------------------------
# LOGIN — Autenticación
# Endpoint: POST /api/auth/login
#
# Puede iniciar sesión usando:
#   - email, o
#   - username
#
# JSON esperado:
# {
#   "email": "example@mail.com",
#   "password": "mypassword"
# }
#   O:
# {
#   "username": "user123",
#   "password": "mypassword"
# }
#
# Si las credenciales son correctas → devuelve un JWT.
#
# Respuesta:
# {
#   "message": "Login successful",
#   "access_token": "JWT_TOKEN_AQUI",
#   "user": {...info del usuario...}
# }
#
# El frontend DEBE guardar ese token y enviarlo así:
# Authorization: Bearer <token>
# ----------------------------------------------------------------------
@auth_bp.route("/login", methods=["POST"])
def auth_login():
    data = request.get_json() or {}

    # Puede identificarse con email o username
    email_or_username = data.get("email") or data.get("username")
    password = data.get("password")

    if not email_or_username or not password:
        return jsonify({"message": "Missing credentials"}), 400

    # Buscar usuario por email o username
    user = User.query.filter(
        (User.email == email_or_username) | (User.username == email_or_username)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Identity del JWT debe ser STRING
    identity = str(user.id)

    # Claims adicionales (se pueden leer luego desde el frontend)
    additional_claims = {
        "role": user.role,
        "username": user.username
    }

    # Generar token JWT
    access_token = create_access_token(
        identity=identity,
        additional_claims=additional_claims
    )

    # Se devuelve también info del usuario para mostrar en el frontend
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role
        }
    }), 200



# ----------------------------------------------------------------------
# ME — Obtener información del usuario autenticado
# Endpoint: GET /api/auth/me
#
# Requiere token:
# Authorization: Bearer <token>
#
# Devuelve el id del usuario del token.
#
# Ejemplo de respuesta:
# {
#   "message": "Current user",
#   "user_id": "3"
# }
#
# El frontend puede usar este endpoint para:
#   - Verificar si el token sigue vivo
#   - Mostrar el usuario actual
#   - Cargar datos iniciales del dashboard
# ----------------------------------------------------------------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def auth_me():
    # Obtiene el user_id guardado como identity en el JWT
    current_user_id = get_jwt_identity()

    return jsonify({
        "message": "Current user",
        "user_id": current_user_id
    }), 200



# ----------------------------------------------------------------------
# PING — Endpoint para probar conectividad del blueprint
# Endpoint: GET /api/auth/ping
#
# Simplemente responde si las rutas de autenticación
# están funcionando correctamente.
#
# Útil para pruebas rápidas del backend.
# ----------------------------------------------------------------------
@auth_bp.route("/ping", methods=["GET"])
def auth_ping():
    """
    Simple endpoint to verify that the auth blueprint is registered.
    """
    return jsonify({"message": "auth blueprint is working"}), 200

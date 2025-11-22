from flask import Blueprint, request, jsonify
from models import db, Donation
from flask_jwt_extended import jwt_required, get_jwt_identity

# Blueprint para todas las rutas relacionadas con donaciones.
# El prefix es /api/donations (registrado en app.py)
donation_bp = Blueprint("donations", __name__)


# ----------------------------------------------------------------------
# CREAR DONACIÓN
# Endpoint: POST /api/donations/
#
# RUTA PROTEGIDA → requiere token JWT
# Header:
#   Authorization: Bearer <token>
#
# Body JSON esperado:
# {
#   "title": "Caja de comida",
#   "description": "Contiene arroz y frijoles",
#   "category": "non_perishable",
#   "quantity": 4
# }
#
# Respuestas:
#   201 → Donación creada correctamente
#   400 → Faltan campos / datos inválidos
#
# NOTA PARA FRONTEND:
# - El backend obtiene automáticamente el donor_id desde el token.
# - El frontend NO debe enviar donor_id.
# ----------------------------------------------------------------------
@donation_bp.route("/", methods=["POST"])
@jwt_required()
def create_donation():
    """
    Crear una donación (solo usuarios logueados).
    El donor_id se toma del token JWT, no del body.
    """
    data = request.get_json() or {}

    title = data.get("title")
    description = data.get("description")
    category = data.get("category")
    quantity = data.get("quantity")

    # Validación de campos necesarios
    if not title or not quantity:
        return jsonify({"message": "Missing required fields"}), 400

    # Validar que quantity sea número
    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({"message": "Quantity must be a number"}), 400

    # Identidad del usuario logueado viene del JWT
    current_user_id = get_jwt_identity()
    try:
        donor_id = int(current_user_id)
    except (TypeError, ValueError):
        return jsonify({"message": "Invalid user id in token"}), 400

    # Crear la donación
    donation = Donation(
        title=title,
        description=description,
        category=category,
        quantity=quantity,
        expiration_date=None,
        donor_id=donor_id,
        status="pending"   # Estado inicial
    )

    db.session.add(donation)
    db.session.commit()

    return jsonify({
        "message": "Donation created successfully",
        "donation": {
            "id": donation.id,
            "title": donation.title,
            "quantity": donation.quantity,
            "status": donation.status
        }
    }), 201



# ----------------------------------------------------------------------
# LISTAR DONACIONES DISPONIBLES
# Endpoint: GET /api/donations/available
#
# RUTA PÚBLICA → no necesita token
#
# El frontend puede usarla para:
#   - mostrar todas las donaciones disponibles
#
# Respuesta:
# [
#   {
#     "id": 1,
#     "title": "Comida enlatada",
#     "quantity": 4,
#     "status": "pending",
#     "donor_id": 2
#   }, ...
# ]
#
# NOTA:
# - Filtramos donaciones rechazadas → no se muestran
# ----------------------------------------------------------------------
@donation_bp.route("/available", methods=["GET"])
def get_available_donations():
    """
    Lista todas las donaciones que NO estén rechazadas.
    Ruta pública.
    """
    donations = Donation.query.filter(Donation.status != "rejected").all()

    result = []
    for d in donations:
        result.append({
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "category": d.category,
            "quantity": d.quantity,
            "status": d.status,
            "donor_id": d.donor_id
        })

    return jsonify(result), 200



# ----------------------------------------------------------------------
# LISTAR MIS DONACIONES
# Endpoint: GET /api/donations/mine
#
# RUTA PROTEGIDA → requiere token JWT
# Header:
#   Authorization: Bearer <token>
#
# Respuesta:
# [
#   {
#     "id": 1,
#     "title": "Caja de comida",
#     "quantity": 4,
#     "status": "pending"
#   }, ...
# ]
#
# El frontend puede usar esta ruta para mostrar:
#   - donaciones creadas por el usuario logueado.
# ----------------------------------------------------------------------
@donation_bp.route("/mine", methods=["GET"])
@jwt_required()
def get_my_donations():
    """
    Listar las donaciones del usuario logueado.
    """
    # Obtener id del usuario desde el token
    current_user_id = get_jwt_identity()

    try:
        donor_id = int(current_user_id)
    except (TypeError, ValueError):
        return jsonify({"message": "Invalid user id in token"}), 400

    # Consultar donaciones del usuario
    donations = Donation.query.filter_by(donor_id=donor_id).all()

    result = []
    for d in donations:
        result.append({
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "category": d.category,
            "quantity": d.quantity,
            "status": d.status
        })

    return jsonify(result), 200

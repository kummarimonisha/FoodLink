from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializo SQLAlchemy.
# Esta instancia se comparte con toda la app (se usa en app.py y en los modelos).
db = SQLAlchemy()


# ---------------------------------------------------------------------
# MODELO: User
# Representa a cada usuario dentro del sistema FoodLink.
# Usuarios pueden ser:
#   - donors      (donan comida)
#   - recipients  (reciben comida)
#   - admin       (opcional, para aprobar donaciones)
# ---------------------------------------------------------------------
class User(db.Model):
    __tablename__ = "users"

    # ID interno del usuario (clave primaria)
    id = db.Column(db.Integer, primary_key=True)

    # Email único, necesario para login.
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Nombre de usuario único (username). También se puede usar para login.
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Contraseña encriptada. Nunca se guarda texto plano.
    password_hash = db.Column(db.String(255), nullable=False)

    # Rol del usuario dentro del sistema:
    #   "donor", "recipient", "admin"
    role = db.Column(db.String(20), nullable=False, default="recipient")

    # Estado del usuario (por si en el futuro hay suspensiones)
    is_active = db.Column(db.Boolean, default=True)

    # Fecha de creación del usuario
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ------------------------------
    # Métodos de utilidad para contraseñas
    # ------------------------------

    def set_password(self, password):
        """
        Recibe la contraseña en texto plano y la convierte en un hash seguro.
        Esto es utilizado en el registro y en la creación de usuarios de prueba.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifica si la contraseña que el usuario envía coincide
        con el hash guardado. Esto se usa en el login.
        """
        return check_password_hash(self.password_hash, password)


# ---------------------------------------------------------------------
# MODELO: Donation
# Representa una donación creada por un usuario con rol "donor".
#
# El frontend usará este modelo para:
#   - Crear donaciones nuevas
#   - Listar donaciones disponibles
#   - Ver las donaciones del usuario actual
#
# El administrador podría aprobar/rechazar donaciones
# mediante el campo "status".
# ---------------------------------------------------------------------
class Donation(db.Model):
    __tablename__ = "donations"

    # ID interno de la donación
    id = db.Column(db.Integer, primary_key=True)

    # Título descriptivo de la donación (obligatorio)
    title = db.Column(db.String(120), nullable=False)

    # Descripción opcional
    description = db.Column(db.Text, nullable=True)

    # Categoría opcional (non_perishable, ready_to_eat, produce, etc.)
    category = db.Column(db.String(50), nullable=True)

    # Cantidad (número de unidades/porciones)
    quantity = db.Column(db.Integer, nullable=False)

    # Fecha de expiración (opcional)
    expiration_date = db.Column(db.DateTime, nullable=True)

    # Estado de la donación:
    #   pending   → recién creada
    #   approved  → aprobada por admin (opcional)
    #   allocated → entregada/asignada a un recipient
    #   rejected  → denegada por admin
    status = db.Column(db.String(20), default="pending")

    # Fecha de creación de la donación
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con el usuario que la creó (donor)
    donor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Objeto usuario asociado a la donación.
    # db.relationship permite acceder a:
    #   donation.donor  → objeto User
    #   user.donations → todas las donaciones del usuario
    donor = db.relationship("User", backref="donations")

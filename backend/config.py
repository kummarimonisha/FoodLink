class Config:
    """
    Configuración principal de la aplicación.
    Esta clase se importa desde app.py para inicializar
    la base de datos, el JWT y cualquier otra configuración global.

    IMPORTANTE:
    En ambiente de producción estas claves se deben mover
    a variables de entorno. Para efectos de la clase y desarrollo local,
    están declaradas directamente aquí.
    """

    # Clave secreta general de Flask.
    # Se usa para firmar cookies y manejar sesiones.
    # El frontend NO necesita conocer esta clave.
    SECRET_KEY = "dev_secret_key"

    # URL de la base de datos.
    # En este caso usamos SQLite local porque el proyecto es académico
    # y no requiere infraestructura externa.
    # Cuando se corre la app, Flask crea automáticamente foodlink.db
    # dentro de la carpeta 'instance/'.
    SQLALCHEMY_DATABASE_URI = "sqlite:///foodlink.db"

    # Mejora de rendimiento: evita que SQLAlchemy rastree cambios innecesarios.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clave secreta utilizada para firmar y validar JWT.
    # El backend la usa para generar los tokens de login.
    # El frontend solo recibe el token, nunca la clave.
    JWT_SECRET_KEY = "jwt_secret_key"

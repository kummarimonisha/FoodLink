class Config:
    """
    Main configuration class for the FoodLink backend.
    Loaded by app.py to configure the database, JWT, and other settings.

    NOTE:
    For production, SECRET_KEY and JWT_SECRET_KEY should be stored
    in environment variables instead of being hardcoded.
    """

    # Flask secret key used for session signing and security.
    SECRET_KEY = "dev_secret_key"

    # SQLite database URL for local development.
    # Flask will store the SQLite file under the instance folder.
    SQLALCHEMY_DATABASE_URI = "sqlite:///foodlink.db"

    # Disable SQLAlchemy modification tracking overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key used to sign and validate JWT tokens.
    # The frontend only receives the token, never this key.
    JWT_SECRET_KEY = "jwt_secret_key"

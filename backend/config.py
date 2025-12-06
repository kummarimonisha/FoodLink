from datetime import timedelta


class Config:
    """
    Basic configuration class for the FoodLink backend.

    app.py imports this class and uses it to configure
    the database, JWT, and other global settings.

    In a real deployment these values should usually come
    from environment variables instead of being hard-coded.
    """

    # Secret key used internally by Flask (sessions, cookies, etc.).
    # For production this should NOT be a fixed string.
    SECRET_KEY = "dev_secret_key"

    # Local SQLite database for development.
    # The file "foodlink.db" will be created in the instance folder.
    SQLALCHEMY_DATABASE_URI = "sqlite:///foodlink.db"

    # Turn off SQLAlchemy's event system to avoid extra overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key used to sign and verify JWT tokens.
    # The client never sees this value, only the tokens it generates.
    JWT_SECRET_KEY = "jwt_secret_key"

    # Access tokens will expire after 1 hour.
    # You can change the number of hours or use minutes/seconds if needed.
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

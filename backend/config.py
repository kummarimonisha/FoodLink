class Config:
    SECRET_KEY = "dev_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///foodlink.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clave para JWT (puede ser distinta si quieres)
    JWT_SECRET_KEY = "jwt_secret_key"   
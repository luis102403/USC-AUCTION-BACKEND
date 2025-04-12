import os
from datetime import timedelta

class Config:
    # DATABASE CONFIGURATION
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT CONFIGURATION
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'tu_clave_jwt_super_secreta')
    # Convertir la variable de entorno a entero para usarla como minutos, por defecto 60 (1 hora)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 60)))

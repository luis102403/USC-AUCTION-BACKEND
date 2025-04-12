# app/services/auth_service.py
from flask_jwt_extended import create_access_token
from flask_injector import inject
from werkzeug.exceptions import Unauthorized
from app.repositories.user_repository import UserRepository
import logging

logger = logging.getLogger(__name__)

class AuthService:
    @inject
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate(self, identifier, password):
        """
        Verifica la identidad del usuario y, si es correcta, genera un token JWT.
        Se usa 'identifier' que puede ser username o email.
        """
        user = self.user_repository.get_by_username_or_email(identifier)
        if not user:
            logger.warning("Usuario no encontrado para el identificador ingresado")
            raise Unauthorized("Credenciales inválidas")

        if user.password != password:
            logger.warning("Contraseña inválida para el usuario")
            raise Unauthorized("Credenciales inválidas")
        
        access_token = create_access_token(identity=user.id)
        return {
            "msg": "Login exitoso",
            "access_token": access_token,
            "user": user.as_dict()
        }

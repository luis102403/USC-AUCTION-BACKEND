# app/controllers/auth_controller.py
from flask import Blueprint, request, jsonify
from flask_injector import inject
from werkzeug.exceptions import BadRequest, Unauthorized
from app.services.auth_service import AuthService
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@inject
def login(auth_service: AuthService):
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("El request debe contener un body en formato JSON.")

        # Permitir el envío de 'username' o 'email' como identificador
        identifier = data.get('username') or data.get('email')
        password = data.get('password')

        if not identifier or not password:
            raise BadRequest("Se requieren 'username' (o 'email') y 'password'.")

        # Se delega la autenticación al servicio
        token_data = auth_service.authenticate(identifier, password)
        return jsonify(token_data), 200

    except BadRequest as e:
        logger.error(f"Error de validación en login: {e}")
        return jsonify({"msg": str(e)}), 400
    except Unauthorized as e:
        logger.warning(f"Login no autorizado para el identificador: {identifier}")
        return jsonify({"msg": str(e)}), 401
    except Exception as e:
        logger.error(f"Error interno en login: {e}")
        return jsonify({"msg": "Ocurrió un error interno"}), 500

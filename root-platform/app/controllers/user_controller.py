# app/controllers/user_controller.py
from flask import Blueprint, request
from flask_injector import inject
from app.services.user_service import UserService
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from app.utils.response import api_response
import logging
logger = logging.getLogger(__name__)
user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['GET'])
@inject
def get_all_users(user_service: UserService):
    try:
        users = user_service.get_all_users()
        return api_response(True, result=users, status=200)
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@inject
def get_user_by_id(user_id, user_service: UserService):
    try:
        user = user_service.get_user_by_id(user_id)
        return api_response(True, result=[user], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@user_bp.route('/users', methods=['POST'])
@inject
def create_user(user_service: UserService):
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        phone = data.get('phone')
        address = data.get('address')
        if not username or not email or not password:
            raise BadRequest("username, email, and password are required")
        user = user_service.create_user(username, email, password, role, phone, address)
        return api_response(True, result=[user], status=201)
    except Conflict as e:
        return api_response(False, status=409, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@inject
def update_user(user_id, user_service: UserService):
    try:
        data = request.json
        user = user_service.update_user(user_id, **data)
        return api_response(True, result=[user], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@inject
def delete_user(user_id, user_service: UserService):
    try:
        resp = user_service.delete_user(user_id)
        return api_response(True, result=resp, status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

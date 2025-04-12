# app/controllers/product_controller.py
from flask import Blueprint, request
from flask_injector import inject
from app.services.product_service import ProductService
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from app.utils.response import api_response
import logging
logger = logging.getLogger(__name__)
product_bp = Blueprint('products', __name__)

@product_bp.route('/products', methods=['GET'])
@inject
def get_all_products(product_service: ProductService):
    try:
        products = product_service.get_all_products()
        return api_response(True, result=products, status=200)
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@product_bp.route('/products/<int:product_id>', methods=['GET'])
@inject
def get_product_by_id(product_id, product_service: ProductService):
    try:
        product = product_service.get_product_by_id(product_id)
        return api_response(True, result=[product], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@product_bp.route('/products', methods=['POST'])
@inject
def create_product(product_service: ProductService):
    try:
        data = request.json
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        stock = data.get('stock')
        low_stock_threshold = data.get('low_stock_threshold')
        image_url = data.get('image_url')
        if not name or price is None or stock is None:
            raise BadRequest("name, price, and stock are required")
        product = product_service.create_product(name, description, price, stock, low_stock_threshold, image_url)
        return api_response(True, result=[product], status=201)
    except Conflict as e:
        return api_response(False, status=409, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
@inject
def update_product(product_id, product_service: ProductService):
    try:
        data = request.json
        product = product_service.update_product(product_id, **data)
        return api_response(True, result=[product], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@inject
def delete_product(product_id, product_service: ProductService):
    try:
        resp = product_service.delete_product(product_id)
        return api_response(True, result=resp, status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

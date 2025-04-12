from flask import Blueprint, request
from flask_injector import inject
from app.services.auction_category_service import AuctionCategoryService
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from app.utils.response import api_response
import logging

logger = logging.getLogger(__name__)
auction_category_bp = Blueprint('auction_categories', __name__)

@auction_category_bp.route('/auction-categories', methods=['GET'])
@inject
def get_all_auction_categories(auction_category_service: AuctionCategoryService):
    try:
        categories = auction_category_service.get_all_auction_categories()
        return api_response(True, result=categories, status=200)
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_category_bp.route('/auction-categories/<int:auction_category_id>', methods=['GET'])
@inject
def get_auction_category_by_id(auction_category_id, auction_category_service: AuctionCategoryService):
    try:
        category = auction_category_service.get_auction_category_by_id(auction_category_id)
        return api_response(True, result=[category], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_category_bp.route('/auction-categories', methods=['POST'])
@inject
def create_auction_category(auction_category_service: AuctionCategoryService):
    try:
        data = request.json
        name = data.get('name')
        description = data.get('description')
        if not name:
            raise BadRequest("Name is required")
        category = auction_category_service.create_auction_category(name, description)
        return api_response(True, result=[category], status=201)
    except Conflict as e:
        return api_response(False, status=409, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_category_bp.route('/auction-categories/<int:auction_category_id>', methods=['PUT'])
@inject
def update_auction_category(auction_category_id, auction_category_service: AuctionCategoryService):
    try:
        data = request.json
        category = auction_category_service.update_auction_category(auction_category_id, **data)
        return api_response(True, result=[category], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_category_bp.route('/auction-categories/<int:auction_category_id>', methods=['DELETE'])
@inject
def delete_auction_category(auction_category_id, auction_category_service: AuctionCategoryService):
    try:
        resp = auction_category_service.delete_auction_category(auction_category_id)
        return api_response(True, result=resp, status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

from flask import Blueprint, request
from flask_injector import inject
from app.services.auction_item_category_service import AuctionItemCategoryService
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from app.utils.response import api_response
import logging

logger = logging.getLogger(__name__)
auction_item_category_bp = Blueprint('auction_item_categories', __name__)

@auction_item_category_bp.route('/auction-item-categories', methods=['GET'])
@inject
def get_all_auction_item_categories(auction_item_category_service: AuctionItemCategoryService):
    try:
        item_categories = auction_item_category_service.get_all_auction_item_categories()
        return api_response(True, result=item_categories, status=200)
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_item_category_bp.route('/auction-item-categories/<int:auction_item_category_id>', methods=['GET'])
@inject
def get_auction_item_category_by_id(auction_item_category_id, auction_item_category_service: AuctionItemCategoryService):
    try:
        item_category = auction_item_category_service.get_auction_item_category_by_id(auction_item_category_id)
        return api_response(True, result=[item_category], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_item_category_bp.route('/auction-item-categories', methods=['POST'])
@inject
def create_auction_item_category(auction_item_category_service: AuctionItemCategoryService):
    try:
        data = request.json
        auction_item_id = data.get('auction_item_id')
        category_id = data.get('category_id')
        if not auction_item_id or not category_id:
            raise BadRequest("auction_item_id and category_id are required")
        item_category = auction_item_category_service.create_auction_item_category(auction_item_id, category_id)
        return api_response(True, result=[item_category], status=201)
    except Conflict as e:
        return api_response(False, status=409, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_item_category_bp.route('/auction-item-categories/<int:auction_item_category_id>', methods=['PUT'])
@inject
def update_auction_item_category(auction_item_category_id, auction_item_category_service: AuctionItemCategoryService):
    try:
        data = request.json
        item_category = auction_item_category_service.update_auction_item_category(auction_item_category_id, **data)
        return api_response(True, result=[item_category], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_item_category_bp.route('/auction-item-categories/<int:auction_item_category_id>', methods=['DELETE'])
@inject
def delete_auction_item_category(auction_item_category_id, auction_item_category_service: AuctionItemCategoryService):
    try:
        resp = auction_item_category_service.delete_auction_item_category(auction_item_category_id)
        return api_response(True, result=resp, status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

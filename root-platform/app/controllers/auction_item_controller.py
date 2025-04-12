from flask import Blueprint, request
from flask_injector import inject
from app.services.auction_item_service import AuctionItemService
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from app.utils.response import api_response
import logging

logger = logging.getLogger(__name__)
auction_item_bp = Blueprint('auction_items', __name__)

@auction_item_bp.route('/auction-items', methods=['GET'])
@inject
def get_all_auction_items(auction_item_service: AuctionItemService):
    try:
        auction_items = auction_item_service.get_all_auction_items()
        return api_response(True, result=auction_items, status=200)
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_item_bp.route('/auction-items/<int:auction_item_id>', methods=['GET'])
@inject
def get_auction_item_by_id(auction_item_id, auction_item_service: AuctionItemService):
    try:
        auction_item = auction_item_service.get_auction_item_by_id(auction_item_id)
        return api_response(True, result=[auction_item], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_item_bp.route('/auction-items', methods=['POST'])
@inject
def create_auction_item(auction_item_service: AuctionItemService):
    try:
        data = request.json
        title = data.get('title')
        description = data.get('description')
        starting_price = data.get('starting_price')
        auction_start = data.get('auction_start')
        auction_end = data.get('auction_end')
        seller_id = data.get('seller_id')
        if not title or starting_price is None or auction_start is None or auction_end is None:
            raise BadRequest("Title, starting_price, auction_start, and auction_end are required")
        auction_item = auction_item_service.create_auction_item(title, description, starting_price, auction_start, auction_end, seller_id)
        return api_response(True, result=[auction_item], status=201)
    except Conflict as e:
        return api_response(False, status=409, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_item_bp.route('/auction-items/<int:auction_item_id>', methods=['PUT'])
@inject
def update_auction_item(auction_item_id, auction_item_service: AuctionItemService):
    try:
        data = request.json
        auction_item = auction_item_service.update_auction_item(auction_item_id, **data)
        return api_response(True, result=[auction_item], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_item_bp.route('/auction-items/<int:auction_item_id>', methods=['DELETE'])
@inject
def delete_auction_item(auction_item_id, auction_item_service: AuctionItemService):
    try:
        resp = auction_item_service.delete_auction_item(auction_item_id)
        return api_response(True, result=resp, status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

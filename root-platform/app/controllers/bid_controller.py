from flask import Blueprint, request
from flask_injector import inject
from app.services.bid_service import BidService
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from app.utils.response import api_response
import logging

logger = logging.getLogger(__name__)
bid_bp = Blueprint('bids', __name__)

@bid_bp.route('/bids', methods=['GET'])
@inject
def get_all_bids(bid_service: BidService):
    try:
        bids = bid_service.get_all_bids()
        return api_response(True, result=bids, status=200)
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@bid_bp.route('/bids/<int:bid_id>', methods=['GET'])
@inject
def get_bid_by_id(bid_id, bid_service: BidService):
    try:
        bid = bid_service.get_bid_by_id(bid_id)
        return api_response(True, result=[bid], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@bid_bp.route('/bids', methods=['POST'])
@inject
def create_bid(bid_service: BidService):
    try:
        data = request.json
        auction_item_id = data.get('auction_item_id')
        bidder_id = data.get('bidder_id')
        bid_amount = data.get('bid_amount')
        if auction_item_id is None or bidder_id is None or bid_amount is None:
            raise BadRequest("auction_item_id, bidder_id, and bid_amount are required")
        bid = bid_service.create_bid(auction_item_id, bidder_id, bid_amount)
        return api_response(True, result=[bid], status=201)
    except Conflict as e:
        return api_response(False, status=409, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@bid_bp.route('/bids/<int:bid_id>', methods=['PUT'])
@inject
def update_bid(bid_id, bid_service: BidService):
    try:
        data = request.json
        bid = bid_service.update_bid(bid_id, **data)
        return api_response(True, result=[bid], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@bid_bp.route('/bids/<int:bid_id>', methods=['DELETE'])
@inject
def delete_bid(bid_id, bid_service: BidService):
    try:
        resp = bid_service.delete_bid(bid_id)
        return api_response(True, result=resp, status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

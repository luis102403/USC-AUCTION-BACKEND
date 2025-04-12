from flask import Blueprint, request
from flask_injector import inject
from app.services.auction_transaction_service import AuctionTransactionService
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from app.utils.response import api_response
import logging

logger = logging.getLogger(__name__)
auction_transaction_bp = Blueprint('auction_transactions', __name__)

@auction_transaction_bp.route('/auction-transactions', methods=['GET'])
@inject
def get_all_auction_transactions(auction_transaction_service: AuctionTransactionService):
    try:
        transactions = auction_transaction_service.get_all_auction_transactions()
        return api_response(True, result=transactions, status=200)
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_transaction_bp.route('/auction-transactions/<int:auction_transaction_id>', methods=['GET'])
@inject
def get_auction_transaction_by_id(auction_transaction_id, auction_transaction_service: AuctionTransactionService):
    try:
        transaction = auction_transaction_service.get_auction_transaction_by_id(auction_transaction_id)
        return api_response(True, result=[transaction], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_transaction_bp.route('/auction-transactions', methods=['POST'])
@inject
def create_auction_transaction(auction_transaction_service: AuctionTransactionService):
    try:
        data = request.json
        auction_item_id = data.get('auction_item_id')
        winner_id = data.get('winner_id')
        final_price = data.get('final_price')
        if not auction_item_id or winner_id is None or final_price is None:
            raise BadRequest("auction_item_id, winner_id, and final_price are required")
        transaction = auction_transaction_service.create_auction_transaction(auction_item_id, winner_id, final_price)
        return api_response(True, result=[transaction], status=201)
    except Conflict as e:
        return api_response(False, status=409, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_transaction_bp.route('/auction-transactions/<int:auction_transaction_id>', methods=['PUT'])
@inject
def update_auction_transaction(auction_transaction_id, auction_transaction_service: AuctionTransactionService):
    try:
        data = request.json
        transaction = auction_transaction_service.update_auction_transaction(auction_transaction_id, **data)
        return api_response(True, result=[transaction], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_transaction_bp.route('/auction-transactions/<int:auction_transaction_id>', methods=['DELETE'])
@inject
def delete_auction_transaction(auction_transaction_id, auction_transaction_service: AuctionTransactionService):
    try:
        resp = auction_transaction_service.delete_auction_transaction(auction_transaction_id)
        return api_response(True, result=resp, status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

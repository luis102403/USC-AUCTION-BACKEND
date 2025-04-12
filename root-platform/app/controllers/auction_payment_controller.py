from flask import Blueprint, request
from flask_injector import inject
from app.services.auction_payment_service import AuctionPaymentService
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from app.utils.response import api_response
import logging

logger = logging.getLogger(__name__)
auction_payment_bp = Blueprint('auction_payments', __name__)

@auction_payment_bp.route('/auction-payments', methods=['GET'])
@inject
def get_all_auction_payments(auction_payment_service: AuctionPaymentService):
    try:
        payments = auction_payment_service.get_all_auction_payments()
        return api_response(True, result=payments, status=200)
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_payment_bp.route('/auction-payments/<int:auction_payment_id>', methods=['GET'])
@inject
def get_auction_payment_by_id(auction_payment_id, auction_payment_service: AuctionPaymentService):
    try:
        payment = auction_payment_service.get_auction_payment_by_id(auction_payment_id)
        return api_response(True, result=[payment], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_payment_bp.route('/auction-payments', methods=['POST'])
@inject
def create_auction_payment(auction_payment_service: AuctionPaymentService):
    try:
        data = request.json
        auction_transaction_id = data.get('auction_transaction_id')
        amount = data.get('amount')
        payment_method = data.get('payment_method')
        if auction_transaction_id is None or amount is None or payment_method is None:
            raise BadRequest("auction_transaction_id, amount, and payment_method are required")
        payment = auction_payment_service.create_auction_payment(auction_transaction_id, amount, payment_method)
        return api_response(True, result=[payment], status=201)
    except Conflict as e:
        return api_response(False, status=409, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_payment_bp.route('/auction-payments/<int:auction_payment_id>', methods=['PUT'])
@inject
def update_auction_payment(auction_payment_id, auction_payment_service: AuctionPaymentService):
    try:
        data = request.json
        payment = auction_payment_service.update_auction_payment(auction_payment_id, **data)
        return api_response(True, result=[payment], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_payment_bp.route('/auction-payments/<int:auction_payment_id>', methods=['DELETE'])
@inject
def delete_auction_payment(auction_payment_id, auction_payment_service: AuctionPaymentService):
    try:
        resp = auction_payment_service.delete_auction_payment(auction_payment_id)
        return api_response(True, result=resp, status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

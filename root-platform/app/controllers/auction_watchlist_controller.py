from flask import Blueprint, request
from flask_injector import inject
from app.services.auction_watchlist_service import AuctionWatchlistService
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from app.utils.response import api_response
import logging

logger = logging.getLogger(__name__)
auction_watchlist_bp = Blueprint('auction_watchlists', __name__)

@auction_watchlist_bp.route('/auction-watchlists', methods=['GET'])
@inject
def get_all_auction_watchlists(auction_watchlist_service: AuctionWatchlistService):
    try:
        watchlists = auction_watchlist_service.get_all_auction_watchlists()
        return api_response(True, result=watchlists, status=200)
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_watchlist_bp.route('/auction-watchlists/<int:auction_watchlist_id>', methods=['GET'])
@inject
def get_auction_watchlist_by_id(auction_watchlist_id, auction_watchlist_service: AuctionWatchlistService):
    try:
        watchlist = auction_watchlist_service.get_auction_watchlist_by_id(auction_watchlist_id)
        return api_response(True, result=[watchlist], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_watchlist_bp.route('/auction-watchlists', methods=['POST'])
@inject
def create_auction_watchlist(auction_watchlist_service: AuctionWatchlistService):
    try:
        data = request.json
        user_id = data.get('user_id')
        auction_item_id = data.get('auction_item_id')
        if not user_id or not auction_item_id:
            raise BadRequest("user_id and auction_item_id are required")
        watchlist = auction_watchlist_service.create_auction_watchlist(user_id, auction_item_id)
        return api_response(True, result=[watchlist], status=201)
    except Conflict as e:
        return api_response(False, status=409, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_watchlist_bp.route('/auction-watchlists/<int:auction_watchlist_id>', methods=['PUT'])
@inject
def update_auction_watchlist(auction_watchlist_id, auction_watchlist_service: AuctionWatchlistService):
    try:
        data = request.json
        watchlist = auction_watchlist_service.update_auction_watchlist(auction_watchlist_id, **data)
        return api_response(True, result=[watchlist], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_watchlist_bp.route('/auction-watchlists/<int:auction_watchlist_id>', methods=['DELETE'])
@inject
def delete_auction_watchlist(auction_watchlist_id, auction_watchlist_service: AuctionWatchlistService):
    try:
        resp = auction_watchlist_service.delete_auction_watchlist(auction_watchlist_id)
        return api_response(True, result=resp, status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

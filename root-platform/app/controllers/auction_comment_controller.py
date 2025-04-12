from flask import Blueprint, request
from flask_injector import inject
from app.services.auction_comment_service import AuctionCommentService
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from app.utils.response import api_response
import logging

logger = logging.getLogger(__name__)
auction_comment_bp = Blueprint('auction_comments', __name__)

@auction_comment_bp.route('/auction-comments', methods=['GET'])
@inject
def get_all_auction_comments(auction_comment_service: AuctionCommentService):
    try:
        comments = auction_comment_service.get_all_auction_comments()
        return api_response(True, result=comments, status=200)
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_comment_bp.route('/auction-comments/<int:auction_comment_id>', methods=['GET'])
@inject
def get_auction_comment_by_id(auction_comment_id, auction_comment_service: AuctionCommentService):
    try:
        comment = auction_comment_service.get_auction_comment_by_id(auction_comment_id)
        return api_response(True, result=[comment], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_comment_bp.route('/auction-comments', methods=['POST'])
@inject
def create_auction_comment(auction_comment_service: AuctionCommentService):
    try:
        data = request.json
        auction_item_id = data.get('auction_item_id')
        user_id = data.get('user_id')
        comment = data.get('comment')
        if not auction_item_id or not user_id or not comment:
            raise BadRequest("auction_item_id, user_id, and comment are required")
        new_comment = auction_comment_service.create_auction_comment(auction_item_id, user_id, comment)
        return api_response(True, result=[new_comment], status=201)
    except Conflict as e:
        return api_response(False, status=409, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_comment_bp.route('/auction-comments/<int:auction_comment_id>', methods=['PUT'])
@inject
def update_auction_comment(auction_comment_id, auction_comment_service: AuctionCommentService):
    try:
        data = request.json
        comment = auction_comment_service.update_auction_comment(auction_comment_id, **data)
        return api_response(True, result=[comment], status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except BadRequest as e:
        return api_response(False, status=400, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

@auction_comment_bp.route('/auction-comments/<int:auction_comment_id>', methods=['DELETE'])
@inject
def delete_auction_comment(auction_comment_id, auction_comment_service: AuctionCommentService):
    try:
        resp = auction_comment_service.delete_auction_comment(auction_comment_id)
        return api_response(True, result=resp, status=200)
    except NotFound as e:
        return api_response(False, status=404, message=str(e))
    except Exception as e:
        return api_response(False, status=500, message="An internal error occurred")

from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
import logging
from app.models.auction_comment import AuctionComment
from app.repositories.auction_comment_repository import AuctionCommentRepository

logger = logging.getLogger(__name__)

class AuctionCommentService:
    @inject
    def __init__(self, auction_comment_repository: AuctionCommentRepository):
        self.auction_comment_repository = auction_comment_repository

    def get_all_auction_comments(self):
        try:
            comments = self.auction_comment_repository.get_all()
            return [comment.as_dict() for comment in comments]
        except Exception as e:
            logger.error(f"Error retrieving auction comments: {e}")
            raise BadRequest(f"Error retrieving auction comments: {str(e)}")

    def get_auction_comment_by_id(self, auction_comment_id):
        comment = self.auction_comment_repository.get_by_id(auction_comment_id)
        if not comment:
            logger.warning(f"Auction comment not found with ID: {auction_comment_id}")
            raise NotFound(f"Auction comment with ID {auction_comment_id} not found")
        return comment.as_dict()

    def create_auction_comment(self, auction_item_id, user_id, comment, comment_date=None, created_by=None):
        auction_comment = AuctionComment(auction_item_id, user_id, comment, comment_date, created_by)
        new_comment = self.auction_comment_repository.create(auction_comment)
        return new_comment.as_dict()

    def update_auction_comment(self, auction_comment_id, **kwargs):
        comment = self.auction_comment_repository.get_by_id(auction_comment_id)
        if not comment:
            logger.warning(f"Auction comment not found with ID: {auction_comment_id}")
            raise NotFound(f"Auction comment with ID {auction_comment_id} not found")
        for key, value in kwargs.items():
            setattr(comment, key, value)
        self.auction_comment_repository.update()
        return comment.as_dict()

    def delete_auction_comment(self, auction_comment_id):
        comment = self.auction_comment_repository.get_by_id(auction_comment_id)
        if not comment:
            logger.warning(f"Auction comment not found with ID: {auction_comment_id}")
            raise NotFound(f"Auction comment with ID {auction_comment_id} not found")
        self.auction_comment_repository.delete(comment)
        return {"message": f"Auction comment with ID {auction_comment_id} deleted"}

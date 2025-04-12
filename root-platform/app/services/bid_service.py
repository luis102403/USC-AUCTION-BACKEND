from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
import logging
from app.models.bid import Bid
from app.repositories.bid_repository import BidRepository

logger = logging.getLogger(__name__)

class BidService:
    @inject
    def __init__(self, bid_repository: BidRepository):
        self.bid_repository = bid_repository

    def get_all_bids(self):
        try:
            bids = self.bid_repository.get_all()
            return [bid.as_dict() for bid in bids]
        except Exception as e:
            logger.error(f"Error retrieving bids: {e}")
            raise BadRequest(f"Error retrieving bids: {str(e)}")

    def get_bid_by_id(self, bid_id):
        bid = self.bid_repository.get_by_id(bid_id)
        if not bid:
            logger.warning(f"Bid not found with ID: {bid_id}")
            raise NotFound(f"Bid with ID {bid_id} not found")
        return bid.as_dict()

    def create_bid(self, auction_item_id, bidder_id, bid_amount):
        bid = Bid(auction_item_id, bidder_id, bid_amount)
        new_bid = self.bid_repository.create(bid)
        return new_bid.as_dict()

    def update_bid(self, bid_id, **kwargs):
        bid = self.bid_repository.get_by_id(bid_id)
        if not bid:
            logger.warning(f"Bid not found with ID: {bid_id}")
            raise NotFound(f"Bid with ID {bid_id} not found")
        for key, value in kwargs.items():
            setattr(bid, key, value)
        self.bid_repository.update()
        return bid.as_dict()

    def delete_bid(self, bid_id):
        bid = self.bid_repository.get_by_id(bid_id)
        if not bid:
            logger.warning(f"Bid not found with ID: {bid_id}")
            raise NotFound(f"Bid with ID {bid_id} not found")
        self.bid_repository.delete(bid)
        return {"message": f"Bid with ID {bid_id} deleted"}

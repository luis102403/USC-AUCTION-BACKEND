from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
import logging
from app.models.auction_item import AuctionItem
from app.repositories.auction_item_repository import AuctionItemRepository

logger = logging.getLogger(__name__)

class AuctionItemService:
    @inject
    def __init__(self, auction_item_repository: AuctionItemRepository):
        self.auction_item_repository = auction_item_repository

    def get_all_auction_items(self):
        try:
            auction_items = self.auction_item_repository.get_all()
            return [auction_item.as_dict() for auction_item in auction_items]
        except Exception as e:
            logger.error(f"Error retrieving auction items: {e}")
            raise BadRequest(f"Error retrieving auction items: {str(e)}")

    def get_auction_item_by_id(self, auction_item_id):
        auction_item = self.auction_item_repository.get_by_id(auction_item_id)
        if not auction_item:
            logger.warning(f"Auction item not found with ID: {auction_item_id}")
            raise NotFound(f"Auction item with ID {auction_item_id} not found")
        return auction_item.as_dict()

    def create_auction_item(self, title, description, starting_price, auction_start, auction_end, seller_id, reserve_price=None, buy_now_price=None, image_url=None, created_by=None):
        auction_item = AuctionItem(title, description, starting_price, auction_start, auction_end, seller_id, reserve_price, buy_now_price, image_url, created_by)
        new_auction_item = self.auction_item_repository.create(auction_item)
        return new_auction_item.as_dict()

    def update_auction_item(self, auction_item_id, **kwargs):
        auction_item = self.auction_item_repository.get_by_id(auction_item_id)
        if not auction_item:
            logger.warning(f"Auction item not found with ID: {auction_item_id}")
            raise NotFound(f"Auction item with ID {auction_item_id} not found")
        for key, value in kwargs.items():
            setattr(auction_item, key, value)
        self.auction_item_repository.update()
        return auction_item.as_dict()

    def delete_auction_item(self, auction_item_id):
        auction_item = self.auction_item_repository.get_by_id(auction_item_id)
        if not auction_item:
            logger.warning(f"Auction item not found with ID: {auction_item_id}")
            raise NotFound(f"Auction item with ID {auction_item_id} not found")
        self.auction_item_repository.delete(auction_item)
        return {"message": f"Auction item with ID {auction_item_id} deleted"}

from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
import logging
from app.models.auction_item_category import AuctionItemCategory
from app.repositories.auction_item_category_repository import AuctionItemCategoryRepository

logger = logging.getLogger(__name__)

class AuctionItemCategoryService:
    @inject
    def __init__(self, auction_item_category_repository: AuctionItemCategoryRepository):
        self.auction_item_category_repository = auction_item_category_repository

    def get_all_auction_item_categories(self):
        try:
            item_categories = self.auction_item_category_repository.get_all()
            return [item_category.as_dict() for item_category in item_categories]
        except Exception as e:
            logger.error(f"Error retrieving auction item categories: {e}")
            raise BadRequest(f"Error retrieving auction item categories: {str(e)}")

    def get_auction_item_category_by_id(self, auction_item_category_id):
        item_category = self.auction_item_category_repository.get_by_id(auction_item_category_id)
        if not item_category:
            logger.warning(f"Auction item category not found with ID: {auction_item_category_id}")
            raise NotFound(f"Auction item category with ID {auction_item_category_id} not found")
        return item_category.as_dict()

    def create_auction_item_category(self, auction_item_id, category_id, created_by=None):
        item_category = AuctionItemCategory(auction_item_id, category_id, created_by)
        new_item_category = self.auction_item_category_repository.create(item_category)
        return new_item_category.as_dict()

    def update_auction_item_category(self, auction_item_category_id, **kwargs):
        item_category = self.auction_item_category_repository.get_by_id(auction_item_category_id)
        if not item_category:
            logger.warning(f"Auction item category not found with ID: {auction_item_category_id}")
            raise NotFound(f"Auction item category with ID {auction_item_category_id} not found")
        for key, value in kwargs.items():
            setattr(item_category, key, value)
        self.auction_item_category_repository.update()
        return item_category.as_dict()

    def delete_auction_item_category(self, auction_item_category_id):
        item_category = self.auction_item_category_repository.get_by_id(auction_item_category_id)
        if not item_category:
            logger.warning(f"Auction item category not found with ID: {auction_item_category_id}")
            raise NotFound(f"Auction item category with ID {auction_item_category_id} not found")
        self.auction_item_category_repository.delete(item_category)
        return {"message": f"Auction item category with ID {auction_item_category_id} deleted"}

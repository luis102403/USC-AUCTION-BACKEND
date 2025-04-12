from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
import logging
from app.models.auction_category import AuctionCategory
from app.repositories.auction_category_repository import AuctionCategoryRepository

logger = logging.getLogger(__name__)

class AuctionCategoryService:
    @inject
    def __init__(self, auction_category_repository: AuctionCategoryRepository):
        self.auction_category_repository = auction_category_repository

    def get_all_auction_categories(self):
        try:
            categories = self.auction_category_repository.get_all()
            return [category.as_dict() for category in categories]
        except Exception as e:
            logger.error(f"Error retrieving auction categories: {e}")
            raise BadRequest(f"Error retrieving auction categories: {str(e)}")

    def get_auction_category_by_id(self, auction_category_id):
        category = self.auction_category_repository.get_by_id(auction_category_id)
        if not category:
            logger.warning(f"Auction category not found with ID: {auction_category_id}")
            raise NotFound(f"Auction category with ID {auction_category_id} not found")
        return category.as_dict()

    def create_auction_category(self, name, description=None, created_by=None):
        category = AuctionCategory(name, description, created_by)
        new_category = self.auction_category_repository.create(category)
        return new_category.as_dict()

    def update_auction_category(self, auction_category_id, **kwargs):
        category = self.auction_category_repository.get_by_id(auction_category_id)
        if not category:
            logger.warning(f"Auction category not found with ID: {auction_category_id}")
            raise NotFound(f"Auction category with ID {auction_category_id} not found")
        for key, value in kwargs.items():
            setattr(category, key, value)
        self.auction_category_repository.update()
        return category.as_dict()

    def delete_auction_category(self, auction_category_id):
        category = self.auction_category_repository.get_by_id(auction_category_id)
        if not category:
            logger.warning(f"Auction category not found with ID: {auction_category_id}")
            raise NotFound(f"Auction category with ID {auction_category_id} not found")
        self.auction_category_repository.delete(category)
        return {"message": f"Auction category with ID {auction_category_id} deleted"}

from app.models.auction_item_category import AuctionItemCategory
from app.extensions import db

class AuctionItemCategoryRepository:
    @staticmethod
    def get_all():
        return AuctionItemCategory.query.all()

    @staticmethod
    def get_by_id(auction_item_category_id):
        return AuctionItemCategory.query.get(auction_item_category_id)

    @staticmethod
    def create(auction_item_category):
        db.session.add(auction_item_category)
        db.session.commit()
        return auction_item_category

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(auction_item_category):
        db.session.delete(auction_item_category)
        db.session.commit()

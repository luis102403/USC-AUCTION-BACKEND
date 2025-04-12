from app.models.auction_category import AuctionCategory
from app.extensions import db

class AuctionCategoryRepository:
    @staticmethod
    def get_all():
        return AuctionCategory.query.all()

    @staticmethod
    def get_by_id(auction_category_id):
        return AuctionCategory.query.get(auction_category_id)

    @staticmethod
    def create(auction_category):
        db.session.add(auction_category)
        db.session.commit()
        return auction_category

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(auction_category):
        db.session.delete(auction_category)
        db.session.commit()

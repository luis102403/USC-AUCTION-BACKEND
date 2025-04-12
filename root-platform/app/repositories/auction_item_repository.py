from app.models.auction_item import AuctionItem
from app.extensions import db

class AuctionItemRepository:
    @staticmethod
    def get_all():
        return AuctionItem.query.all()

    @staticmethod
    def get_by_id(auction_item_id):
        return AuctionItem.query.get(auction_item_id)

    @staticmethod
    def create(auction_item):
        db.session.add(auction_item)
        db.session.commit()
        return auction_item

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(auction_item):
        db.session.delete(auction_item)
        db.session.commit()

from app.models.bid import Bid
from app.extensions import db

class BidRepository:
    @staticmethod
    def get_all():
        return Bid.query.all()

    @staticmethod
    def get_by_id(bid_id):
        return Bid.query.get(bid_id)

    @staticmethod
    def create(bid):
        db.session.add(bid)
        db.session.commit()
        return bid

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(bid):
        db.session.delete(bid)
        db.session.commit()

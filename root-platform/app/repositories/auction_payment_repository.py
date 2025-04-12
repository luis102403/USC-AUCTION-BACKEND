from app.models.auction_payment import AuctionPayment
from app.extensions import db

class AuctionPaymentRepository:
    @staticmethod
    def get_all():
        return AuctionPayment.query.all()

    @staticmethod
    def get_by_id(auction_payment_id):
        return AuctionPayment.query.get(auction_payment_id)

    @staticmethod
    def create(auction_payment):
        db.session.add(auction_payment)
        db.session.commit()
        return auction_payment

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(auction_payment):
        db.session.delete(auction_payment)
        db.session.commit()

from app.models.auction_transaction import AuctionTransaction
from app.extensions import db

class AuctionTransactionRepository:
    @staticmethod
    def get_all():
        return AuctionTransaction.query.all()

    @staticmethod
    def get_by_id(auction_transaction_id):
        return AuctionTransaction.query.get(auction_transaction_id)

    @staticmethod
    def create(auction_transaction):
        db.session.add(auction_transaction)
        db.session.commit()
        return auction_transaction

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(auction_transaction):
        db.session.delete(auction_transaction)
        db.session.commit()

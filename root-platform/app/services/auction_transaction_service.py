from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
import logging
from app.models.auction_transaction import AuctionTransaction
from app.repositories.auction_transaction_repository import AuctionTransactionRepository

logger = logging.getLogger(__name__)

class AuctionTransactionService:
    @inject
    def __init__(self, auction_transaction_repository: AuctionTransactionRepository):
        self.auction_transaction_repository = auction_transaction_repository

    def get_all_auction_transactions(self):
        try:
            transactions = self.auction_transaction_repository.get_all()
            return [transaction.as_dict() for transaction in transactions]
        except Exception as e:
            logger.error(f"Error retrieving auction transactions: {e}")
            raise BadRequest(f"Error retrieving auction transactions: {str(e)}")

    def get_auction_transaction_by_id(self, auction_transaction_id):
        transaction = self.auction_transaction_repository.get_by_id(auction_transaction_id)
        if not transaction:
            logger.warning(f"Auction transaction not found with ID: {auction_transaction_id}")
            raise NotFound(f"Auction transaction with ID {auction_transaction_id} not found")
        return transaction.as_dict()

    def create_auction_transaction(self, auction_item_id, winner_id, final_price):
        transaction = AuctionTransaction(auction_item_id, winner_id, final_price)
        new_transaction = self.auction_transaction_repository.create(transaction)
        return new_transaction.as_dict()

    def update_auction_transaction(self, auction_transaction_id, **kwargs):
        transaction = self.auction_transaction_repository.get_by_id(auction_transaction_id)
        if not transaction:
            logger.warning(f"Auction transaction not found with ID: {auction_transaction_id}")
            raise NotFound(f"Auction transaction with ID {auction_transaction_id} not found")
        for key, value in kwargs.items():
            setattr(transaction, key, value)
        self.auction_transaction_repository.update()
        return transaction.as_dict()

    def delete_auction_transaction(self, auction_transaction_id):
        transaction = self.auction_transaction_repository.get_by_id(auction_transaction_id)
        if not transaction:
            logger.warning(f"Auction transaction not found with ID: {auction_transaction_id}")
            raise NotFound(f"Auction transaction with ID {auction_transaction_id} not found")
        self.auction_transaction_repository.delete(transaction)
        return {"message": f"Auction transaction with ID {auction_transaction_id} deleted"}

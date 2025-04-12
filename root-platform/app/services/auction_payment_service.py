from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
import logging
from app.models.auction_payment import AuctionPayment
from app.repositories.auction_payment_repository import AuctionPaymentRepository

logger = logging.getLogger(__name__)

class AuctionPaymentService:
    @inject
    def __init__(self, auction_payment_repository: AuctionPaymentRepository):
        self.auction_payment_repository = auction_payment_repository

    def get_all_auction_payments(self):
        try:
            payments = self.auction_payment_repository.get_all()
            return [payment.as_dict() for payment in payments]
        except Exception as e:
            logger.error(f"Error retrieving auction payments: {e}")
            raise BadRequest(f"Error retrieving auction payments: {str(e)}")

    def get_auction_payment_by_id(self, auction_payment_id):
        payment = self.auction_payment_repository.get_by_id(auction_payment_id)
        if not payment:
            logger.warning(f"Auction payment not found with ID: {auction_payment_id}")
            raise NotFound(f"Auction payment with ID {auction_payment_id} not found")
        return payment.as_dict()

    def create_auction_payment(self, auction_transaction_id, amount, payment_method, status='pending'):
        payment = AuctionPayment(auction_transaction_id, amount, payment_method, status)
        new_payment = self.auction_payment_repository.create(payment)
        return new_payment.as_dict()

    def update_auction_payment(self, auction_payment_id, **kwargs):
        payment = self.auction_payment_repository.get_by_id(auction_payment_id)
        if not payment:
            logger.warning(f"Auction payment not found with ID: {auction_payment_id}")
            raise NotFound(f"Auction payment with ID {auction_payment_id} not found")
        for key, value in kwargs.items():
            setattr(payment, key, value)
        self.auction_payment_repository.update()
        return payment.as_dict()

    def delete_auction_payment(self, auction_payment_id):
        payment = self.auction_payment_repository.get_by_id(auction_payment_id)
        if not payment:
            logger.warning(f"Auction payment not found with ID: {auction_payment_id}")
            raise NotFound(f"Auction payment with ID {auction_payment_id} not found")
        self.auction_payment_repository.delete(payment)
        return {"message": f"Auction payment with ID {auction_payment_id} deleted"}

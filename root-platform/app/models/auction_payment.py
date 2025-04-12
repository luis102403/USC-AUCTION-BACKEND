from app.extensions import db
from datetime import datetime

class AuctionPayment(db.Model):
    __tablename__ = 'auction_payment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auction_transaction_id = db.Column(db.Integer, db.ForeignKey('auction_transaction.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime)

    auction_transaction = db.relationship('AuctionTransaction', backref='payments')

    def __init__(self, auction_transaction_id, amount, payment_date=None, payment_method=None, status='pending', created_by=None, created_at=None, updated_by=None, updated_at=None):
        self.auction_transaction_id = auction_transaction_id
        self.amount = amount
        self.payment_date = payment_date if payment_date else datetime.utcnow()
        self.payment_method = payment_method
        self.status = status
        self.created_by = created_by
        self.created_at = created_at if created_at else datetime.utcnow()
        self.updated_by = updated_by
        self.updated_at = updated_at

    def as_dict(self):
        return {
            'id': self.id,
            'auction_transaction_id': self.auction_transaction_id,
            'amount': str(self.amount),
            'payment_date': self.payment_date.isoformat(),
            'payment_method': self.payment_method,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_by': self.updated_by,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

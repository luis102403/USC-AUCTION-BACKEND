from app.extensions import db
from datetime import datetime

class AuctionTransaction(db.Model):
    __tablename__ = 'auction_transaction'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auction_item_id = db.Column(db.Integer, db.ForeignKey('auction_item.id'), nullable=False)  # Referencia al ítem subastado
    winner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Usuario ganador de la subasta
    final_price = db.Column(db.Numeric(10, 2), nullable=False)  # Precio final de la subasta
    transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Fecha de realización de la transacción
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime)

    # Relación con el ganador (ya está ajustado el backref)
    winner = db.relationship('User', backref='transactions', foreign_keys=[winner_id])

    def __init__(self, auction_item_id, winner_id, final_price, transaction_date=None, created_by=None, created_at=None, updated_by=None, updated_at=None):
        self.auction_item_id = auction_item_id
        self.winner_id = winner_id
        self.final_price = final_price
        self.transaction_date = transaction_date if transaction_date else datetime.utcnow()
        self.created_by = created_by
        self.created_at = created_at if created_at else datetime.utcnow()
        self.updated_by = updated_by
        self.updated_at = updated_at

    def as_dict(self):
        return {
            'id': self.id,
            'auction_item_id': self.auction_item_id,
            'winner_id': self.winner_id,
            'final_price': str(self.final_price),
            'transaction_date': self.transaction_date.isoformat(),
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_by': self.updated_by,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

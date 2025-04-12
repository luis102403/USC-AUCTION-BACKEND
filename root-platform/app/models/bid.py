from app.extensions import db
from datetime import datetime

class Bid(db.Model):
    __tablename__ = 'bid'
    
    # Definición de las columnas de la tabla
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auction_item_id = db.Column(db.Integer, db.ForeignKey('auction_item.id'), nullable=False)  # Referencia al producto subastado
    bidder_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Usuario que realiza la oferta
    bid_amount = db.Column(db.Numeric(10, 2), nullable=False)  # Monto ofertado
    bid_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Fecha y hora en que se realiza la oferta
    created_by = db.Column(db.Integer)  # Usuario que crea la puja
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha y hora de creación
    updated_by = db.Column(db.Integer)  # Usuario que actualiza la puja
    updated_at = db.Column(db.DateTime)  # Fecha y hora de la última actualización

    # Relaciones con las otras tablas
    auction_item = db.relationship('AuctionItem', backref='bids')  # Relación con la tabla `auction_item`
    bidder = db.relationship('User', backref='bids')  # Relación con la tabla `users` (usuario que puja)

    def __init__(self, auction_item_id, bidder_id, bid_amount, bid_time=None, created_by=None, created_at=None, updated_by=None, updated_at=None):
        self.auction_item_id = auction_item_id
        self.bidder_id = bidder_id
        self.bid_amount = bid_amount
        self.bid_time = bid_time if bid_time else datetime.utcnow()
        self.created_by = created_by
        self.created_at = created_at if created_at else datetime.utcnow()
        self.updated_by = updated_by
        self.updated_at = updated_at

    def as_dict(self):
        return {
            'id': self.id,
            'auction_item_id': self.auction_item_id,
            'bidder_id': self.bidder_id,
            'bid_amount': str(self.bid_amount),
            'bid_time': self.bid_time.isoformat(),
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_by': self.updated_by,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

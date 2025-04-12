from app.extensions import db
from datetime import datetime

class AuctionItem(db.Model):
    __tablename__ = 'auction_item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    starting_price = db.Column(db.Numeric(10, 2), nullable=False)  # Precio de inicio de la subasta
    reserve_price = db.Column(db.Numeric(10, 2))  # Precio de reserva
    buy_now_price = db.Column(db.Numeric(10, 2))  # Precio de "compra inmediata"
    auction_start = db.Column(db.DateTime, nullable=False)
    auction_end = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')  # 'active', 'closed', 'cancelled'
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Referencia al vendedor
    image_url = db.Column(db.String(255))
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime)

    seller = db.relationship('User', backref='auction_items')

    def __init__(self, title, description, starting_price, auction_start, auction_end, seller_id, reserve_price=None, buy_now_price=None, image_url=None, created_by=None, created_at=None, updated_by=None, updated_at=None):
        self.title = title
        self.description = description
        self.starting_price = starting_price
        self.auction_start = auction_start
        self.auction_end = auction_end
        self.seller_id = seller_id
        self.reserve_price = reserve_price
        self.buy_now_price = buy_now_price
        self.image_url = image_url
        self.created_by = created_by
        self.created_at = created_at if created_at is not None else datetime.utcnow()
        self.updated_by = updated_by
        self.updated_at = updated_at

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'starting_price': str(self.starting_price),
            'reserve_price': str(self.reserve_price) if self.reserve_price else None,
            'buy_now_price': str(self.buy_now_price) if self.buy_now_price else None,
            'auction_start': self.auction_start.isoformat(),
            'auction_end': self.auction_end.isoformat(),
            'status': self.status,
            'seller_id': self.seller_id,
            'image_url': self.image_url,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_by': self.updated_by,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

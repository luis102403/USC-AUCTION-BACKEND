from app.extensions import db
from datetime import datetime

class AuctionItemCategory(db.Model):
    __tablename__ = 'auction_item_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auction_item_id = db.Column(db.Integer, db.ForeignKey('auction_item.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('auction_category.id'), nullable=False)
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime)

    auction_item = db.relationship('AuctionItem', backref='item_categories')
    category = db.relationship('AuctionCategory', backref='item_categories')

    def __init__(self, auction_item_id, category_id, created_by=None, created_at=None, updated_by=None, updated_at=None):
        self.auction_item_id = auction_item_id
        self.category_id = category_id
        self.created_by = created_by
        self.created_at = created_at if created_at is not None else datetime.utcnow()
        self.updated_by = updated_by
        self.updated_at = updated_at

    def as_dict(self):
        return {
            'id': self.id,
            'auction_item_id': self.auction_item_id,
            'category_id': self.category_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_by': self.updated_by,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

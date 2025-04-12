from app.extensions import db
from datetime import datetime

class AuctionComment(db.Model):
    __tablename__ = 'auction_comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auction_item_id = db.Column(db.Integer, db.ForeignKey('auction_item.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime)

    user = db.relationship('User', backref='comments')
    auction_item = db.relationship('AuctionItem', backref='comments')

    def __init__(self, auction_item_id, user_id, comment, comment_date=None, created_by=None, created_at=None, updated_by=None, updated_at=None):
        self.auction_item_id = auction_item_id
        self.user_id = user_id
        self.comment = comment
        self.comment_date = comment_date if comment_date else datetime.utcnow()
        self.created_by = created_by
        self.created_at = created_at if created_at is not None else datetime.utcnow()
        self.updated_by = updated_by
        self.updated_at = updated_at

    def as_dict(self):
        return {
            'id': self.id,
            'auction_item_id': self.auction_item_id,
            'user_id': self.user_id,
            'comment': self.comment,
            'comment_date': self.comment_date.isoformat(),
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_by': self.updated_by,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

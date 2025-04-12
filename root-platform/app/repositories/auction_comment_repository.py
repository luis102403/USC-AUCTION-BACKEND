from app.models.auction_comment import AuctionComment
from app.extensions import db

class AuctionCommentRepository:
    @staticmethod
    def get_all():
        return AuctionComment.query.all()

    @staticmethod
    def get_by_id(auction_comment_id):
        return AuctionComment.query.get(auction_comment_id)

    @staticmethod
    def create(auction_comment):
        db.session.add(auction_comment)
        db.session.commit()
        return auction_comment

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(auction_comment):
        db.session.delete(auction_comment)
        db.session.commit()

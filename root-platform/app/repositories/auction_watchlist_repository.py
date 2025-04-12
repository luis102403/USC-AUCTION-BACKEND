from app.models.auction_watchlist import AuctionWatchlist
from app.extensions import db

class AuctionWatchlistRepository:
    @staticmethod
    def get_all():
        return AuctionWatchlist.query.all()

    @staticmethod
    def get_by_id(auction_watchlist_id):
        return AuctionWatchlist.query.get(auction_watchlist_id)

    @staticmethod
    def create(auction_watchlist):
        db.session.add(auction_watchlist)
        db.session.commit()
        return auction_watchlist

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(auction_watchlist):
        db.session.delete(auction_watchlist)
        db.session.commit()

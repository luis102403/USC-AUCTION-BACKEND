from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
import logging
from app.models.auction_watchlist import AuctionWatchlist
from app.repositories.auction_watchlist_repository import AuctionWatchlistRepository

logger = logging.getLogger(__name__)

class AuctionWatchlistService:
    @inject
    def __init__(self, auction_watchlist_repository: AuctionWatchlistRepository):
        self.auction_watchlist_repository = auction_watchlist_repository

    def get_all_auction_watchlists(self):
        try:
            watchlists = self.auction_watchlist_repository.get_all()
            return [watchlist.as_dict() for watchlist in watchlists]
        except Exception as e:
            logger.error(f"Error retrieving auction watchlists: {e}")
            raise BadRequest(f"Error retrieving auction watchlists: {str(e)}")

    def get_auction_watchlist_by_id(self, auction_watchlist_id):
        watchlist = self.auction_watchlist_repository.get_by_id(auction_watchlist_id)
        if not watchlist:
            logger.warning(f"Auction watchlist not found with ID: {auction_watchlist_id}")
            raise NotFound(f"Auction watchlist with ID {auction_watchlist_id} not found")
        return watchlist.as_dict()

    def create_auction_watchlist(self, user_id, auction_item_id, created_by=None):
        watchlist = AuctionWatchlist(user_id, auction_item_id, created_by)
        new_watchlist = self.auction_watchlist_repository.create(watchlist)
        return new_watchlist.as_dict()

    def update_auction_watchlist(self, auction_watchlist_id, **kwargs):
        watchlist = self.auction_watchlist_repository.get_by_id(auction_watchlist_id)
        if not watchlist:
            logger.warning(f"Auction watchlist not found with ID: {auction_watchlist_id}")
            raise NotFound(f"Auction watchlist with ID {auction_watchlist_id} not found")
        for key, value in kwargs.items():
            setattr(watchlist, key, value)
        self.auction_watchlist_repository.update()
        return watchlist.as_dict()

    def delete_auction_watchlist(self, auction_watchlist_id):
        watchlist = self.auction_watchlist_repository.get_by_id(auction_watchlist_id)
        if not watchlist:
            logger.warning(f"Auction watchlist not found with ID: {auction_watchlist_id}")
            raise NotFound(f"Auction watchlist with ID {auction_watchlist_id} not found")
        self.auction_watchlist_repository.delete(watchlist)
        return {"message": f"Auction watchlist with ID {auction_watchlist_id} deleted"}

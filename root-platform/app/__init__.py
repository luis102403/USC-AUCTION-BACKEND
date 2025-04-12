from flask import Flask, jsonify
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import singleton
import logging

from .extensions import db, init_logging, jwt

# Controllers
from .controllers.user_controller import user_bp
from .controllers.auction_item_controller import auction_item_bp
from .controllers.bid_controller import bid_bp
from .controllers.auction_transaction_controller import auction_transaction_bp
from .controllers.auction_payment_controller import auction_payment_bp
from .controllers.auction_category_controller import auction_category_bp
from .controllers.auction_item_category_controller import auction_item_category_bp
from .controllers.auction_watchlist_controller import auction_watchlist_bp
from .controllers.auction_comment_controller import auction_comment_bp
from .controllers.auth_controller import auth_bp

# Services
from .services.user_service import UserService
from .services.auction_item_service import AuctionItemService
from .services.bid_service import BidService
from .services.auction_transaction_service import AuctionTransactionService
from .services.auction_payment_service import AuctionPaymentService
from .services.auction_category_service import AuctionCategoryService
from .services.auction_item_category_service import AuctionItemCategoryService
from .services.auction_watchlist_service import AuctionWatchlistService
from .services.auction_comment_service import AuctionCommentService
from .services.auth_service import AuthService

def configure(binder):
    binder.bind(UserService, to=UserService, scope=singleton)
    binder.bind(AuctionItemService, to=AuctionItemService, scope=singleton)
    binder.bind(BidService, to=BidService, scope=singleton)
    binder.bind(AuctionTransactionService, to=AuctionTransactionService, scope=singleton)
    binder.bind(AuctionPaymentService, to=AuctionPaymentService, scope=singleton)
    binder.bind(AuctionCategoryService, to=AuctionCategoryService, scope=singleton)
    binder.bind(AuctionItemCategoryService, to=AuctionItemCategoryService, scope=singleton)
    binder.bind(AuctionWatchlistService, to=AuctionWatchlistService, scope=singleton)
    binder.bind(AuctionCommentService, to=AuctionCommentService, scope=singleton)
    binder.bind(AuthService, to=AuthService, scope=singleton)

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('app.config.Config')

    # Inicializa la base de datos y JWTManager
    db.init_app(app)
    jwt.init_app(app)  # Inicializamos JWTManager

    logger = init_logging()
    logger.info("API Initialized")  

    # Register Blueprints
    app.register_blueprint(user_bp, url_prefix='/api/v1')
    app.register_blueprint(auction_item_bp, url_prefix='/api/v1')
    app.register_blueprint(bid_bp, url_prefix='/api/v1/bids')
    app.register_blueprint(auction_transaction_bp, url_prefix='/api/v1/auction-transactions')
    app.register_blueprint(auction_payment_bp, url_prefix='/api/v1/auction-payments')
    app.register_blueprint(auction_category_bp, url_prefix='/api/v1/auction-categories')
    app.register_blueprint(auction_item_category_bp, url_prefix='/api/v1/auction-item-categories')
    app.register_blueprint(auction_watchlist_bp, url_prefix='/api/v1/auction-watchlists')
    app.register_blueprint(auction_comment_bp, url_prefix='/api/v1/auction-comments')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    FlaskInjector(app=app, modules=[configure])

    @app.route('/health')
    def health_check():
        logger.info("Health check passed")
        return jsonify({'status': 'Healthy'}), 200

    return app

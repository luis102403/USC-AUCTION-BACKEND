from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import logging

db = SQLAlchemy()
jwt = JWTManager()

def init_logging():
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(__name__)
    return logger

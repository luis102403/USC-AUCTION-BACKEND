from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
import logging
from app.models.product import Product
from app.repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)

class ProductService:
    @inject
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def get_all_products(self):
        try:
            products = self.product_repository.get_all()
            return [product.as_dict() for product in products]
        except Exception as e:
            logger.error(f"Error retrieving products: {e}")
            raise BadRequest(f"Error retrieving products: {str(e)}")

    def get_product_by_id(self, product_id):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            logger.warning(f"Product not found with ID: {product_id}")
            raise NotFound(f"Product with ID {product_id} not found")
        return product.as_dict()

    def create_product(self, name, description, price, stock, low_stock_threshold=None, image_url=None, created_by=None):
        product = Product(name, description, price, stock, low_stock_threshold, image_url, created_by)
        new_product = self.product_repository.create(product)
        return new_product.as_dict()

    def update_product(self, product_id, **kwargs):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            logger.warning(f"Product not found with ID: {product_id}")
            raise NotFound(f"Product with ID {product_id} not found")
        for key, value in kwargs.items():
            setattr(product, key, value)
        self.product_repository.update()
        return product.as_dict()

    def delete_product(self, product_id):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            logger.warning(f"Product not found with ID: {product_id}")
            raise NotFound(f"Product with ID {product_id} not found")
        self.product_repository.delete(product)
        return {"message": f"Product with ID {product_id} deleted"}

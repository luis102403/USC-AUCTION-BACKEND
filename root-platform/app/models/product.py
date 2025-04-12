from app.extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10,2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    low_stock_threshold = db.Column(db.Integer)  # Threshold for low stock alert
    image_url = db.Column(db.String(255))
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime)

    # Relaciones
    inventory_movements = db.relationship('InventoryMovement', backref='product', lazy=True)
    sale_details = db.relationship('SaleDetail', backref='product', lazy=True)
    product_suppliers = db.relationship('ProductSupplier', backref='product', lazy=True)

    def __init__(self, name, description, price, stock, low_stock_threshold=None, image_url=None,
                 created_by=None, created_at=None, updated_by=None, updated_at=None):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.low_stock_threshold = low_stock_threshold
        self.image_url = image_url
        self.created_by = created_by
        self.created_at = created_at if created_at is not None else datetime.utcnow()
        self.updated_by = updated_by
        self.updated_at = updated_at

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': str(self.price),
            'stock': self.stock,
            'low_stock_threshold': self.low_stock_threshold,
            'image_url': self.image_url,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_by': self.updated_by,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
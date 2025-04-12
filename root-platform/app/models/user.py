from app.extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    # Definición de las columnas de la tabla
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Hash de la contraseña
    role = db.Column(db.String(50), nullable=False, default='bidder')  # Roles: 'admin', 'seller', 'bidder'
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime)


    def __init__(self, username, email, password, role='bidder', phone=None, address=None, created_by=None, created_at=None, updated_by=None, updated_at=None):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.phone = phone
        self.address = address
        self.created_by = created_by
        self.created_at = created_at if created_at is not None else datetime.utcnow()
        self.updated_by = updated_by
        self.updated_at = updated_at

    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
            'address': self.address,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_by': self.updated_by,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    category = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)

    def to_dict(self):
        """Serializes the object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "brand": self.brand,
            "price": self.price,
            "stock_quantity": self.stock_quantity,
            "sku": self.sku
        }
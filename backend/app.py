import random
import os
from flask import Flask, request, jsonify
from models import db, Product
from faker import Faker
from sqlalchemy import or_
from flask_cors import CORS

app = Flask(__name__)
# Configure the database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance/data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Enable Cross-Origin Resource Sharing (CORS) for the frontend
CORS(app)

# Initialize Faker for data generation
fake = Faker()

@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables."""
    with app.app_context():
        db.create_all()
    print("Initialized the database.")


@app.route('/products/generate', methods=['POST'])
def generate_products():
    """
    Generates and stores product records in the database.
    Accepts optional 'count' and 'seed' JSON parameters.
    """
    data = request.get_json() or {}
    count = data.get('count', 100)
    seed_val = data.get('seed')

    if seed_val:
        Faker.seed(seed_val)
        random.seed(seed_val)

    products = []
    existing_skus = {p.sku for p in Product.query.with_entities(Product.sku).all()}

    for _ in range(count):
        sku = fake.unique.ean(length=13)
        while sku in existing_skus:
            sku = fake.unique.ean(length=13)
        existing_skus.add(sku)
        
        product = Product(
            name=fake.word(),
            description=fake.text(max_nb_chars=200),
            category=fake.word(),
            brand=fake.company(),
            price=round(random.uniform(10.0, 500.0), 2),
            stock_quantity=random.randint(0, 1000),
            sku=sku
        )
        products.append(product)

    # Use bulk_save_objects for efficient insertion (handles the optional 1000+ challenge)
    db.session.bulk_save_objects(products)
    db.session.commit()

    return jsonify({"message": f"Successfully generated and stored {len(products)} products."}), 201

@app.route('/products', methods=['GET'])
def get_all_products():
    """Returns a list of all product records."""
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/products/search', methods=['GET'])
def search_products():
    """
    Returns a filtered list of products based on a search query.
    Searches across name, description, category, brand, and SKU.
    """
    query_term = request.args.get('q', '').strip()
    if not query_term:
        return jsonify([])

    search_pattern = f"%{query_term}%"
    
    # Optimized query using OR across indexed fields (if indexes were added)
    products = Product.query.filter(
        or_(
            Product.name.ilike(search_pattern),
            Product.description.ilike(search_pattern),
            Product.category.ilike(search_pattern),
            Product.brand.ilike(search_pattern),
            Product.sku.ilike(search_pattern)
        )
    ).all()
    
    return jsonify([p.to_dict() for p in products])

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Ensure db is created when run directly
    app.run(debug=True)
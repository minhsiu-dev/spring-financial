import pytest
from app import app, db, Product

@pytest.fixture
def client():
    """Configures the app for testing and provides a test client."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        # Add sample data for testing
        p1 = Product(name="Laptop Pro", description="A powerful laptop", category="Electronics", brand="TechCorp", price=1200.0, stock_quantity=50, sku="TC-LP-PRO-01")
        p2 = Product(name="Wireless Mouse", description="An ergonomic mouse", category="Accessories", brand="TechCorp", price=25.0, stock_quantity=200, sku="TC-WM-ERG-02")
        p3 = Product(name="Mechanical Keyboard", description="A pro gamer keyboard", category="Accessories", brand="GameGear", price=150.0, stock_quantity=100, sku="GG-MK-RGB-03")
        db.session.add_all([p1, p2, p3])
        db.session.commit()

    yield client

    with app.app_context():
        db.drop_all()

def test_search_endpoint_found(client):
    """Test searching for a term that exists in multiple products."""
    response = client.get('/products/search?q=pro')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2 # "Laptop Pro" and "pro gamer keyboard"
    assert "Laptop Pro" in [p['name'] for p in data]
    assert "Mechanical Keyboard" in [p['name'] for p in data]

def test_search_endpoint_single_result_sku(client):
    """Test searching by a unique SKU."""
    response = client.get('/products/search?q=TC-WM-ERG-02')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == "Wireless Mouse"

def test_search_endpoint_not_found(client):
    """Test searching for a term that does not exist."""
    response = client.get('/products/search?q=nonexistent')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0

def test_search_endpoint_empty_query(client):
    """Test that an empty search query returns an empty list."""
    response = client.get('/products/search?q=')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0
import pytest
from application import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_get_inventory(client):
    response = client.get('/inventory/')
    assert response.status_code == 200

def test_add_inventory(client):
    data = {
        "name": "Brake Pad",
        "price": 29.99
    }
    response = client.post('/inventory/', json=data)
    assert response.status_code == 201

def test_add_inventory_missing_field(client):
    data = {
        "name": "Oil Filter"
        # Missing price
    }
    response = client.post('/inventory/', json=data)
    assert response.status_code == 400
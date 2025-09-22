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

def test_get_customers(client):
    response = client.get('/customers/')
    assert response.status_code == 200

def test_add_customer(client):
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "password": "password123"
    }
    response = client.post('/customers/', json=data)
    assert response.status_code == 201

def test_add_customer_missing_field(client):
    data = {
        "name": "Jane Doe",
        "email": "jane@example.com"
        # Missing phone and password
    }
    response = client.post('/customers/', json=data)
    assert response.status_code == 400
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

def test_get_tickets(client):
    response = client.get('/tickets/')
    assert response.status_code == 200

def test_add_ticket_missing_field(client):
    data = {
        "vin": "1HGCM82633A004352"
        # Missing service_date, service_description, customer_id
    }
    response = client.post('/tickets/', json=data)
    assert response.status_code == 400
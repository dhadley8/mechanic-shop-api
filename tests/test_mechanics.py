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

def test_get_mechanics(client):
    response = client.get('/mechanics/')
    assert response.status_code == 200

def test_add_mechanic_missing_field(client):
    data = {
        "name": "Mike"
        # Missing email, phone, salary
    }
    response = client.post('/mechanics/', json=data)
    assert response.status_code == 400
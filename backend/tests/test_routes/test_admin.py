import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app('testing')  # Assuming you have a testing config
    with app.test_client() as client:
        with app.app_context():
            # You can add setup here, like creating database tables
            yield client
        # Teardown happens here automatically

def test_completed_matches_route(client):
    response = client.get('/matches/completed')
    assert response.status_code == 200
    assert b'Scraping completed and data stored successfully' in response.data

def test_upcoming_matches_route(client):
    response = client.get('/matches/upcoming')
    assert response.status_code == 200
    assert b'Scraping completed and data stored successfully' in response.data

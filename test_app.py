import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    """Test the home endpoint returns correct response."""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "Hello from Jenkins Pipeline!"
    assert data['status'] == "running"
    assert data['version'] == "1.0.0"


def test_health(client):
    """Test the health endpoint returns healthy status."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "healthy"


def test_info(client):
    """Test the info endpoint returns app information."""
    response = client.get('/info')
    assert response.status_code == 200
    data = response.get_json()
    assert data['app'] == "jenkins-pipeline-demo"
    assert 'description' in data
    assert data['author'] == "Aland Khalil"
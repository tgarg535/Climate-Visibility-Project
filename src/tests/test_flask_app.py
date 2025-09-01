
import pytest
from flask import session
from flask_app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test'
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'WeatherPro' in response.data

def test_set_location(client):
    response = client.get('/set_location?lat=28.6&lon=77.2')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'ok'
    assert json_data['lat'] == '28.6'
    assert json_data['lon'] == '77.2'

def test_weather_no_location(client):
    response = client.get('/weather')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Location not set'

def test_forecast_no_location(client):
    response = client.get('/forecast')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Location not provided'

def test_air_pollution_no_location(client):
    response = client.get('/air_pollution')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Location not set'

def test_manual_search_missing_city(client):
    response = client.post('/manual_search', json={})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'City is required'
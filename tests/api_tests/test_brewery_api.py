import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from http_client import HttpClient


@pytest.fixture(scope="module")
def brewery_api_client():
    client = HttpClient("https://api.openbrewerydb.org/v1")
    yield client
    client.close()


def test_list_breweries(brewery_api_client):
    response = brewery_api_client.get("/breweries")
    
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    brewery = data[0]
    assert "id" in brewery
    assert "name" in brewery
    assert "brewery_type" in brewery
    
    assert isinstance(brewery["id"], str)
    assert isinstance(brewery["name"], str)
    assert brewery["brewery_type"] in ["micro", "nano", "regional", "brewpub", "large", "planning", "bar", "contract", "proprietor", "closed"]


def test_get_brewery_by_id(brewery_api_client):

    list_response = brewery_api_client.get("/breweries")
    breweries = list_response.json()
    brewery_id = breweries[0]["id"]
    
    response = brewery_api_client.get(f"/breweries/{brewery_id}")
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == brewery_id
    assert "name" in data
    assert "brewery_type" in data
    assert "city" in data
    assert "state" in data
    
    assert len(data["name"]) > 0


def test_brewery_data_structure(brewery_api_client):
    response = brewery_api_client.get("/breweries")
    
    assert response.status_code == 200
    
    data = response.json()
    brewery = data[0]
    
    required_fields = ["id", "name", "brewery_type", "city", "state", "country"]
    for field in required_fields:
        assert field in brewery, f"Поле {field} отсутствует"
        
    assert brewery["country"] in ["United States", "England", "Scotland", "Ireland", "France", "Germany", "South Korea", "Singapore", "Poland", "Austria", "Portugal"]


@pytest.mark.parametrize("city", ["san_diego", "boston", "portland"])
def test_search_by_city_parametrized(city, brewery_api_client):
    response = brewery_api_client.get("/breweries", params={"by_city": city})
    
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    
    if len(data) > 0:
        for brewery in data[:3]:
            assert "city" in brewery
            assert city.replace("_", " ").lower() in brewery["city"].lower() or brewery["city"].lower() in city.replace("_", " ").lower()


@pytest.mark.parametrize("state", ["california", "texas", "new_york"])
def test_search_by_state_parametrized(state, brewery_api_client):
    response = brewery_api_client.get("/breweries", params={"by_state": state})
    
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    
    if len(data) > 0:
        brewery = data[0]
        assert "state" in brewery
        assert "name" in brewery
        assert "brewery_type" in brewery

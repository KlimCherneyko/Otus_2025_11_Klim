import pytest
import requests


BASE_URL = "https://api.openbrewerydb.org/v1"


def test_list_breweries():
    response = requests.get(f"{BASE_URL}/breweries")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]
    assert "name" in data[0]


def test_get_brewery_by_id():

    list_response = requests.get(f"{BASE_URL}/breweries")
    breweries = list_response.json()
    brewery_id = breweries[0]["id"]
    
    response = requests.get(f"{BASE_URL}/breweries/{brewery_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == brewery_id
    assert "name" in data
    assert "brewery_type" in data


def test_brewery_data_structure():
    response = requests.get(f"{BASE_URL}/breweries")
    assert response.status_code == 200
    data = response.json()
    brewery = data[0]
    required_fields = ["id", "name", "brewery_type", "city", "state", "country"]
    for field in required_fields:
        assert field in brewery


@pytest.mark.parametrize("city", ["san_diego", "boston", "portland"])
def test_search_by_city_parametrized(city):
    response = requests.get(f"{BASE_URL}/breweries", params={"by_city": city})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.parametrize("state", ["california", "texas", "new_york"])
def test_search_by_state_parametrized(state):
    response = requests.get(f"{BASE_URL}/breweries", params={"by_state": state})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

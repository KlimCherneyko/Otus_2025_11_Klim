import pytest
import requests


BASE_URL = "https://dog.ceo/api"


def test_list_all_breeds():
    response = requests.get(f"{BASE_URL}/breeds/list/all")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data
    assert isinstance(data["message"], dict)
    assert len(data["message"]) > 0


def test_random_dog_image():
    response = requests.get(f"{BASE_URL}/breeds/image/random")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"].startswith("https://")


def test_response_structure():
    response = requests.get(f"{BASE_URL}/breeds/list/all")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert response.headers["Content-Type"].startswith("application/json")


@pytest.mark.parametrize("breed", ["hound", "retriever", "bulldog"])
def test_breed_images_parametrized(breed):
    response = requests.get(f"{BASE_URL}/breed/{breed}/images")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["message"], list)
    assert len(data["message"]) > 0


@pytest.mark.parametrize("breed", ["invalidbreed123", "notexist", "fakedog"])
def test_invalid_breed_handling(breed):
    response = requests.get(f"{BASE_URL}/breed/{breed}/images")
    assert response.status_code == 404

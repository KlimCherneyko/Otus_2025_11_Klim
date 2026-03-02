import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from http_client import HttpClient


@pytest.fixture(scope="module")
def dog_api_client():
    client = HttpClient("https://dog.ceo/api")
    yield client
    client.close()


def test_list_all_breeds(dog_api_client):
    response = dog_api_client.get("/breeds/list/all")
    
    assert response.status_code == 200
    
    assert response.headers["Content-Type"].startswith("application/json")
    
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data
    assert isinstance(data["message"], dict)
    
    breeds = data["message"]
    assert len(breeds) > 0
    assert "hound" in breeds
    assert "retriever" in breeds
    
    assert isinstance(breeds["hound"], list)
    assert len(breeds["hound"]) > 0


def test_random_dog_image(dog_api_client):
    response = dog_api_client.get("/breeds/image/random")
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data
    assert isinstance(data["message"], str)
    
    image_url = data["message"]
    assert image_url.startswith("https://")
    assert "images.dog.ceo" in image_url
    assert image_url.endswith((".jpg", ".jpeg", ".png"))


def test_response_structure(dog_api_client):
    response = dog_api_client.get("/breeds/list/all")
    
    assert response.status_code == 200
    
    assert "Content-Type" in response.headers
    assert response.headers["Content-Type"].startswith("application/json")
    
    data = response.json()
    assert "status" in data
    assert "message" in data
    
    assert response.elapsed.total_seconds() < 5


@pytest.mark.parametrize("breed", ["hound", "retriever", "bulldog"])
def test_breed_images_parametrized(breed, dog_api_client):
    response = dog_api_client.get(f"/breed/{breed}/images")
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["message"], list)
    
    images = data["message"]
    assert len(images) > 0
    
    for image_url in images[:5]:
        assert image_url.startswith("https://")
        assert breed in image_url.lower()


@pytest.mark.parametrize("breed", ["invalidbreed123", "notexist", "fakedog"])
def test_invalid_breed_handling(breed, dog_api_client):
    response = dog_api_client.get(f"/breed/{breed}/images")
    
    assert response.status_code == 404
    
    data = response.json()
    assert data["status"] == "error"
    assert "message" in data

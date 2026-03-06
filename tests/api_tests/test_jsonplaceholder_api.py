import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from http_client import HttpClient


@pytest.fixture(scope="module")
def jsonplaceholder_client():
    client = HttpClient("https://jsonplaceholder.typicode.com")
    yield client
    client.close()


def test_list_posts(jsonplaceholder_client):
    response = jsonplaceholder_client.get("/posts")
    
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 100
    
    post = data[0]
    assert post["userId"] == 1
    assert post["id"] == 1
    assert post["title"] == "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
    assert "quia et suscipit" in post["body"]
    
    assert isinstance(post["userId"], int)
    assert isinstance(post["id"], int)
    assert isinstance(post["title"], str)
    assert isinstance(post["body"], str)
    
    assert len(post["title"]) > 0
    assert len(post["body"]) > 0


def test_list_users(jsonplaceholder_client):
    response = jsonplaceholder_client.get("/users")
    
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 10
    
    user = data[0]
    assert user["id"] == 1
    assert user["name"] == "Leanne Graham"
    assert user["username"] == "Bret"
    assert user["email"] == "Sincere@april.biz"
    
    assert "@" in user["email"]
    assert "." in user["email"]
    
    assert isinstance(user["address"], dict)
    assert user["address"]["city"] == "Gwenborough"
    assert user["address"]["street"] == "Kulas Light"


def test_post_data_structure(jsonplaceholder_client):
    response = jsonplaceholder_client.get("/posts/1")
    
    assert response.status_code == 200
    
    data = response.json()
    required_fields = ["userId", "id", "title", "body"]
    for field in required_fields:
        assert field in data
    
    assert data["userId"] == 1
    assert data["id"] == 1
    assert data["title"] == "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
    assert "quia et suscipit" in data["body"]
    
    assert isinstance(data["userId"], int)
    assert isinstance(data["id"], int)
    assert isinstance(data["title"], str)
    assert isinstance(data["body"], str)


@pytest.mark.parametrize("post_id", [1, 5, 10, 50, 100])
def test_get_post_by_id_parametrized(post_id, jsonplaceholder_client):
    response = jsonplaceholder_client.get(f"/posts/{post_id}")
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == post_id
    assert "title" in data
    assert "body" in data
    assert "userId" in data
    
    assert len(data["title"]) > 0
    assert len(data["body"]) > 0
    
    assert isinstance(data["userId"], int)
    assert data["userId"] > 0


@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_comments_parametrized(post_id, jsonplaceholder_client):
    response = jsonplaceholder_client.get("/comments", params={"postId": post_id})
    
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    for comment in data:
        assert comment["postId"] == post_id
        assert "id" in comment
        assert "email" in comment
        assert "body" in comment
        assert "name" in comment
        
        assert "@" in comment["email"]
        
        assert len(comment["body"]) > 0

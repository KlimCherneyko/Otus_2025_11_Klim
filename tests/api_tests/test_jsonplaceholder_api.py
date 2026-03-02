import pytest
import requests


BASE_URL = "https://jsonplaceholder.typicode.com"


def test_list_posts():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "userId" in data[0]
    assert "id" in data[0]
    assert "title" in data[0]
    assert "body" in data[0]


def test_list_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]
    assert "name" in data[0]
    assert "email" in data[0]


def test_post_data_structure():
    response = requests.get(f"{BASE_URL}/posts/1")
    assert response.status_code == 200
    data = response.json()
    required_fields = ["userId", "id", "title", "body"]
    for field in required_fields:
        assert field in data
    assert isinstance(data["userId"], int)
    assert isinstance(data["id"], int)
    assert isinstance(data["title"], str)
    assert isinstance(data["body"], str)


@pytest.mark.parametrize("post_id", [1, 5, 10, 50, 100])
def test_get_post_by_id_parametrized(post_id):
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert "title" in data
    assert "body" in data


@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_comments_parametrized(post_id):
    response = requests.get(f"{BASE_URL}/comments", params={"postId": post_id})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for comment in data:
        assert comment["postId"] == post_id
        assert "id" in comment
        assert "email" in comment
        assert "body" in comment

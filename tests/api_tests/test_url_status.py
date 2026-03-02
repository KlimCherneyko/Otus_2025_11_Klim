"""Тест для проверки статус-кода URL с параметрами через pytest.addoption"""
import pytest
import requests


@pytest.fixture
def url_config(pytestconfig):
    """Фикстура для получения URL и статус-кода из параметров командной строки"""
    return {
        "url": pytestconfig.getoption("url"),
        "status_code": int(pytestconfig.getoption("status_code"))
    }


def test_url_status_code(url_config):
    """Тест проверки статус-кода для заданного URL"""
    url = url_config["url"]
    expected_status_code = url_config["status_code"]
    
    response = requests.get(url, allow_redirects=True)
    assert response.status_code == expected_status_code, \
        f"Ожидался статус-код {expected_status_code}, получен {response.status_code}"

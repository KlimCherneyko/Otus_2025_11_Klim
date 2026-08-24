import pytest

from ui.data import PASSWORD, STANDARD_USER
from ui.pages.inventory_page import InventoryPage
from ui.pages.login_page import LoginPage


@pytest.fixture()
def login_page(driver, base_url: str) -> LoginPage:
    page = LoginPage(driver, base_url)
    page.open()
    return page


@pytest.fixture()
def inventory_page(login_page: LoginPage, driver, base_url: str) -> InventoryPage:
    login_page.login(STANDARD_USER, PASSWORD)
    page = InventoryPage(driver, base_url)
    page.wait_loaded()
    return page

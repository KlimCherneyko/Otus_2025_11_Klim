import allure
import pytest

from ui.data import LOCKED_OUT_USER, PASSWORD, STANDARD_USER
from ui.pages.inventory_page import InventoryPage
from ui.pages.login_page import LoginPage


@allure.feature("UI")
@allure.story("Authentication")
@allure.title("Successful login as standard_user")
def test_successful_login(login_page: LoginPage, driver, base_url: str) -> None:
    login_page.login(STANDARD_USER, PASSWORD)
    inventory = InventoryPage(driver, base_url)
    inventory.wait_loaded()
    assert inventory.is_displayed(inventory.INVENTORY_CONTAINER)


@allure.feature("UI")
@allure.story("Authentication")
@allure.title("Locked out user cannot log in")
def test_locked_out_user(login_page: LoginPage) -> None:
    login_page.login(LOCKED_OUT_USER, PASSWORD)
    assert "locked out" in login_page.get_error_text().lower()


@allure.feature("UI")
@allure.story("Authentication")
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("", PASSWORD, "Username is required"),
        (STANDARD_USER, "", "Password is required"),
        (STANDARD_USER, "wrong_password", "do not match"),
    ],
)
def test_login_validation(
    login_page: LoginPage,
    username: str,
    password: str,
    expected_error: str,
) -> None:
    allure.dynamic.title(f"Login validation: '{expected_error}'")
    login_page.login(username, password)
    assert expected_error.lower() in login_page.get_error_text().lower()


@allure.feature("UI")
@allure.story("Authentication")
@allure.title("User can log out from inventory")
def test_logout(inventory_page: InventoryPage, driver, base_url: str) -> None:
    inventory_page.logout()
    login_page = LoginPage(driver, base_url)
    assert login_page.is_displayed(login_page.LOGIN_BUTTON)

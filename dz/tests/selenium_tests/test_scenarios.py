import time

import allure
import pytest

from tests.pages.admin_login_page import AdminLoginPage
from tests.pages.admin_product_page import AdminProductPage
from tests.pages.catalog_page import CatalogPage
from tests.pages.main_page import MainPage
from tests.pages.registration_page import RegistrationPage


def _unique_suffix() -> str:
    return str(int(time.time() * 1000))


@allure.feature("Admin scenarios")
@allure.story("Authentication")
@allure.title("Admin login and logout")
def test_admin_login_logout(driver, base_url, admin_credentials):
    page = AdminLoginPage(driver, base_url)
    page.open()
    page.login(*admin_credentials)
    page.wait_for_dashboard()
    page.logout()
    page.wait_for_login_page()
    assert page.wait_visible(page.LOGIN_BUTTON).is_displayed()


@allure.feature("Admin scenarios")
@allure.story("Product management")
@allure.title("Admin can add a new product")
def test_admin_add_product(driver, base_url, admin_session):
    page = AdminProductPage(driver, base_url, admin_session.get_user_token())
    suffix = _unique_suffix()
    name = f"AutoTest Product {suffix}"
    message = page.add_product(name, f"AT-{suffix}")
    assert "You have modified products" in message
    assert page.product_exists(name)


@allure.feature("Admin scenarios")
@allure.story("Product management")
@allure.title("Admin can delete a product")
def test_admin_delete_product(driver, base_url, admin_session):
    page = AdminProductPage(driver, base_url, admin_session.get_user_token())
    suffix = _unique_suffix()
    name = f"AutoTest Product {suffix}"
    page.add_product(name, f"AT-{suffix}")
    message = page.delete_product(name)
    assert "You have modified products" in message
    assert not page.product_exists(name)


@allure.feature("Customer scenarios")
@allure.story("Registration")
@allure.title("New customer registration")
def test_register_new_customer(driver, base_url):
    page = RegistrationPage(driver, base_url)
    page.open()
    suffix = _unique_suffix()
    page.register(
        first_name="Auto",
        last_name="Tester",
        email=f"autotest_{suffix}@example.com",
        password="Password123",
    )
    assert "created" in page.wait_for_success().lower()


@allure.feature("Customer scenarios")
@allure.story("Shopping cart")
@allure.title("Add product to cart from main page")
def test_add_product_to_cart_page_from_main_page(driver, base_url):
    page = MainPage(driver, base_url)
    page.open()
    added_product = page.add_first_product_to_cart()
    page.open_cart_page()
    cart_page_items = page.cart_page_items()
    assert added_product in cart_page_items


@allure.feature("Customer scenarios")
@allure.story("Currency")
@allure.title("Currency switch changes prices on {page_class.__name__}")
@pytest.mark.parametrize(
    "page_class,currency,expected_symbol",
    [
        (MainPage, "Euro", "€"),
        (CatalogPage, "Pound Sterling", "£"),
    ],
)
def test_currency_switch_changes_prices(driver, base_url, page_class, currency, expected_symbol):
    page = page_class(driver, base_url)
    page.open()
    initial_prices, updated_prices = page.switch_currency_and_get_updated_prices(currency)
    assert initial_prices != updated_prices
    assert any(expected_symbol in price for price in updated_prices)

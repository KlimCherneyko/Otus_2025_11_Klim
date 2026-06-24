import time

from tests.pages.admin_login_page import AdminLoginPage
from tests.pages.admin_product_page import AdminProductPage
from tests.pages.catalog_page import CatalogPage
from tests.pages.main_page import MainPage
from tests.pages.registration_page import RegistrationPage


def _unique_suffix() -> str:
    return str(int(time.time() * 1000))


def test_admin_login_logout(driver, base_url, admin_credentials):
    page = AdminLoginPage(driver, base_url)
    page.open()
    page.login(*admin_credentials)
    page.wait_for_dashboard()
    page.logout()
    page.wait_visible(page.LOGIN_BUTTON)


def test_admin_add_product(driver, base_url, admin_session):
    page = AdminProductPage(driver, base_url, admin_session.get_user_token())
    suffix = _unique_suffix()
    name = f"AutoTest Product {suffix}"
    message = page.add_product(name, f"AT-{suffix}")
    assert "You have modified products" in message
    assert page.product_exists(name)


def test_admin_delete_product(driver, base_url, admin_session):
    page = AdminProductPage(driver, base_url, admin_session.get_user_token())
    suffix = _unique_suffix()
    name = f"AutoTest Product {suffix}"
    page.add_product(name, f"AT-{suffix}")
    message = page.delete_product(name)
    assert "You have modified products" in message
    assert not page.product_exists(name)


def test_register_new_customer(driver, base_url):
    page = RegistrationPage(driver, base_url)
    page.open()
    suffix = _unique_suffix()
    page.register(
        first_name="Auto",
        last_name="Tester",
        email=f"autotest_{suffix}@example.com",
        telephone="1234567890",
        password="Password123",
    )
    assert "successfully created" in page.wait_for_success().lower()


def test_add_random_product_to_cart_from_main_page(driver, base_url):
    page = MainPage(driver, base_url)
    page.open()
    added_product = page.add_random_product_to_cart()
    page.open_cart_page()
    assert added_product in page.cart_page_items()


def test_currency_switch_changes_prices_on_main_page(driver, base_url):
    page = MainPage(driver, base_url)
    page.open()
    initial_prices = page.get_prices_text()
    page.switch_currency("Euro")
    page.wait_until(lambda d: page.get_prices_text() != initial_prices)
    updated_prices = page.get_prices_text()
    assert initial_prices != updated_prices
    assert any("€" in price for price in updated_prices)


def test_currency_switch_changes_prices_in_catalog(driver, base_url):
    page = CatalogPage(driver, base_url)
    page.open()
    initial_prices = page.get_prices_text()
    page.switch_currency("Pound Sterling")
    page.wait_until(lambda d: page.get_prices_text() != initial_prices)
    updated_prices = page.get_prices_text()
    assert initial_prices != updated_prices
    assert any("£" in price for price in updated_prices)

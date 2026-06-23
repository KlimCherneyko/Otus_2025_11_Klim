import os

import pytest

from tests.pages.admin_login_page import AdminLoginPage
from tests.pages.catalog_page import CatalogPage
from tests.pages.main_page import MainPage


def test_admin_login_logout(driver, base_url):
    page = AdminLoginPage(driver, base_url)
    page.open()

    username = os.getenv("OPENCART_ADMIN_USER")
    password = os.getenv("OPENCART_ADMIN_PASSWORD")
    if not username or not password:
        pytest.skip("Set OPENCART_ADMIN_USER and OPENCART_ADMIN_PASSWORD to run admin login scenario")
    page.login(username, password)
    page.wait_for_dashboard()

    page.logout()
    page.wait_visible(page.LOGIN_BUTTON)


def test_add_random_product_to_cart_from_main_page(driver, base_url):
    page = MainPage(driver, base_url)
    page.open()

    added_product = page.add_random_product_to_cart()
    page.open_cart_page()
    cart_items = page.cart_page_items()

    assert added_product in cart_items, f"'{added_product}' is missing in cart dropdown"


def test_currency_switch_changes_prices_on_main_page(driver, base_url):
    page = MainPage(driver, base_url)
    page.open()

    initial_prices = page.get_prices_text()
    page.switch_currency("Euro")
    page.wait_until(lambda d: page.get_prices_text() != initial_prices)
    updated_prices = page.get_prices_text()

    assert initial_prices != updated_prices, "Prices on main page did not change after currency switch"
    assert any("€" in price for price in updated_prices), "Updated prices do not contain euro sign"


def test_currency_switch_changes_prices_in_catalog(driver, base_url):
    page = CatalogPage(driver, base_url)
    page.open()

    initial_prices = page.get_prices_text()
    page.switch_currency("Pound Sterling")
    page.wait_until(lambda d: page.get_prices_text() != initial_prices)
    updated_prices = page.get_prices_text()

    assert initial_prices != updated_prices, "Prices in catalog did not change after currency switch"
    assert any("£" in price for price in updated_prices), "Updated catalog prices do not contain pound sign"

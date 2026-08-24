import allure
import pytest

from ui.data import PRODUCT_BACKPACK
from ui.pages.cart_page import CartPage
from ui.pages.checkout_complete_page import CheckoutCompletePage
from ui.pages.checkout_info_page import CheckoutInfoPage
from ui.pages.checkout_overview_page import CheckoutOverviewPage
from ui.pages.inventory_page import InventoryPage


@allure.feature("UI")
@allure.story("Checkout")
@allure.title("Complete checkout happy path")
def test_checkout_happy_path(inventory_page: InventoryPage, driver, base_url: str) -> None:
    inventory_page.add_to_cart(PRODUCT_BACKPACK)
    inventory_page.open_cart()

    cart_page = CartPage(driver, base_url)
    cart_page.wait_loaded()
    cart_page.checkout()

    info_page = CheckoutInfoPage(driver, base_url)
    info_page.wait_loaded()
    info_page.submit("John", "Doe", "12345")

    overview_page = CheckoutOverviewPage(driver, base_url)
    overview_page.wait_loaded()
    assert PRODUCT_BACKPACK in overview_page.get_item_names()
    overview_page.finish()

    complete_page = CheckoutCompletePage(driver, base_url)
    complete_page.wait_loaded()
    assert "thank you for your order" in complete_page.get_header().lower()


@allure.feature("UI")
@allure.story("Checkout")
@pytest.mark.parametrize(
    "first_name, last_name, postal_code, expected_error",
    [
        ("", "Doe", "12345", "First Name is required"),
        ("John", "", "12345", "Last Name is required"),
        ("John", "Doe", "", "Postal Code is required"),
    ],
)
def test_checkout_validation(
    inventory_page: InventoryPage,
    driver,
    base_url: str,
    first_name: str,
    last_name: str,
    postal_code: str,
    expected_error: str,
) -> None:
    allure.dynamic.title(f"Checkout validation: '{expected_error}'")
    inventory_page.add_to_cart(PRODUCT_BACKPACK)
    inventory_page.open_cart()

    cart_page = CartPage(driver, base_url)
    cart_page.wait_loaded()
    cart_page.checkout()

    info_page = CheckoutInfoPage(driver, base_url)
    info_page.wait_loaded()
    info_page.submit(first_name, last_name, postal_code)
    assert expected_error.lower() in info_page.get_error_text().lower()

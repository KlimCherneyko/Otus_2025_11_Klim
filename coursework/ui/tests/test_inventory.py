import allure
import pytest

from ui.data import PRODUCT_BACKPACK, PRODUCT_BIKE_LIGHT
from ui.pages.cart_page import CartPage
from ui.pages.inventory_page import InventoryPage
from ui.pages.product_page import ProductPage


@allure.feature("UI")
@allure.story("Catalog")
@pytest.mark.parametrize(
    "sort_value, kind",
    [
        ("az", "name"),
        ("za", "name"),
        ("lohi", "price"),
        ("hilo", "price"),
    ],
)
def test_sort_products(inventory_page: InventoryPage, sort_value: str, kind: str) -> None:
    allure.dynamic.title(f"Sort products by '{sort_value}'")
    inventory_page.sort_by(sort_value)

    if kind == "name":
        names = inventory_page.get_product_names()
        assert names == sorted(names, reverse=(sort_value == "za"))
    else:
        prices = inventory_page.get_product_prices()
        assert prices == sorted(prices, reverse=(sort_value == "hilo"))


@allure.feature("UI")
@allure.story("Catalog")
@allure.title("Product details match catalog name and price")
def test_product_details_match_catalog(inventory_page: InventoryPage, driver, base_url: str) -> None:
    catalog_price = inventory_page.get_product_price(PRODUCT_BACKPACK)
    inventory_page.open_product(PRODUCT_BACKPACK)

    product_page = ProductPage(driver, base_url)
    product_page.wait_loaded()
    assert product_page.get_name() == PRODUCT_BACKPACK
    assert product_page.get_price() == catalog_price


@allure.feature("UI")
@allure.story("Cart")
@allure.title("Add a single product to cart")
def test_add_single_product_to_cart(inventory_page: InventoryPage, driver, base_url: str) -> None:
    inventory_page.add_to_cart(PRODUCT_BACKPACK)
    assert inventory_page.cart_count() == 1

    inventory_page.open_cart()
    cart_page = CartPage(driver, base_url)
    cart_page.wait_loaded()
    assert PRODUCT_BACKPACK in cart_page.get_item_names()


@allure.feature("UI")
@allure.story("Cart")
@allure.title("Add two products to cart")
def test_add_two_products_to_cart(inventory_page: InventoryPage, driver, base_url: str) -> None:
    inventory_page.add_to_cart(PRODUCT_BACKPACK)
    inventory_page.add_to_cart(PRODUCT_BIKE_LIGHT)
    assert inventory_page.cart_count() == 2

    inventory_page.open_cart()
    cart_page = CartPage(driver, base_url)
    cart_page.wait_loaded()
    names = cart_page.get_item_names()
    assert PRODUCT_BACKPACK in names
    assert PRODUCT_BIKE_LIGHT in names


@allure.feature("UI")
@allure.story("Cart")
@allure.title("Remove product from inventory page")
def test_remove_product_from_inventory(inventory_page: InventoryPage) -> None:
    inventory_page.add_to_cart(PRODUCT_BACKPACK)
    assert inventory_page.cart_count() == 1
    inventory_page.remove_from_inventory(PRODUCT_BACKPACK)
    assert inventory_page.cart_count() == 0


@allure.feature("UI")
@allure.story("Cart")
@allure.title("Remove product from cart page")
def test_remove_product_from_cart(inventory_page: InventoryPage, driver, base_url: str) -> None:
    inventory_page.add_to_cart(PRODUCT_BACKPACK)
    inventory_page.open_cart()

    cart_page = CartPage(driver, base_url)
    cart_page.wait_loaded()
    cart_page.remove_item(PRODUCT_BACKPACK)
    assert cart_page.items_count() == 0

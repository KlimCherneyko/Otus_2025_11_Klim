import allure
from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class ProductPage(BasePage):
    PAGE_TITLE = (By.CSS_SELECTOR, "#content h1")
    MAIN_IMAGE = (By.CSS_SELECTOR, "#content .image img, #content .magnific-popup img")
    PRICE_BLOCK = (By.CSS_SELECTOR, "#content .price-new, #content h2")
    QUANTITY_INPUT = (By.ID, "input-quantity")
    ADD_TO_CART_BUTTON = (By.ID, "button-cart")
    DESCRIPTION_TAB = (By.CSS_SELECTOR, "a[href='#tab-description']")
    REVIEW_TAB = (By.CSS_SELECTOR, "a[href='#tab-review']")
    BREADCRUMB = (By.CSS_SELECTOR, ".breadcrumb")

    @allure.step("Open product page")
    def open(self) -> None:
        super().open("index.php?route=product/product&product_id=43")

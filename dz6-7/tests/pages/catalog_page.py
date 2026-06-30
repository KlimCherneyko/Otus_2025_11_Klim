from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class CatalogPage(BasePage):
    PAGE_TITLE = (By.CSS_SELECTOR, "#content h2")
    SORT_SELECT = (By.ID, "input-sort")
    LIMIT_SELECT = (By.ID, "input-limit")
    BREADCRUMB = (By.CSS_SELECTOR, ".breadcrumb")
    PRICE_VALUES = (By.CSS_SELECTOR, ".product-thumb .price")

    def open(self) -> None:
        super().open("index.php?route=product/category&path=20")

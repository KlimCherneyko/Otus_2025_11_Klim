from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class CatalogPage(BasePage):
    PAGE_TITLE = (By.CSS_SELECTOR, "#content h2")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".product-thumb")
    SORT_SELECT = (By.ID, "input-sort")
    LIMIT_SELECT = (By.ID, "input-limit")
    BREADCRUMB = (By.CSS_SELECTOR, ".breadcrumb")
    PRICE_VALUES = (By.CSS_SELECTOR, ".product-thumb .price")
    CURRENCY_BUTTON = (By.CSS_SELECTOR, "#form-currency .dropdown-toggle")

    def open(self) -> None:
        super().open("index.php?route=product/category&path=20")

    def switch_currency(self, currency_title: str) -> None:
        self.click(self.CURRENCY_BUTTON)
        currency_locator = (
            By.XPATH,
            f"//form[@id='form-currency']//button[contains(normalize-space(), '{currency_title}')]",
        )
        self.click(currency_locator)

    def get_prices_text(self) -> list[str]:
        return [price.text.strip() for price in self.wait_all_visible(self.PRICE_VALUES) if price.text.strip()]

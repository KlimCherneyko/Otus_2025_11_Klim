import allure
from urllib.parse import urlencode

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec

from tests.pages.base_page import BasePage


class AdminProductPage(BasePage):
    ADD_BUTTON = (
        By.CSS_SELECTOR,
        "a[data-bs-original-title='Add New'], a[data-original-title='Add New'], a[title='Add New']",
    )
    SAVE_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-bs-original-title='Save'], button[data-original-title='Save'], button[title='Save']",
    )
    DELETE_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-bs-original-title='Delete'], button[data-original-title='Delete'], button[title='Delete']",
    )
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    PRODUCT_NAME_INPUT = (By.CSS_SELECTOR, "#input-name-1, #input-name1")
    META_TITLE_INPUT = (By.CSS_SELECTOR, "#input-meta-title-1, #input-meta-title1")
    DATA_TAB = (By.CSS_SELECTOR, "a[href='#tab-data']")
    SEO_TAB = (By.CSS_SELECTOR, "a[href='#tab-seo']")
    MODEL_INPUT = (By.ID, "input-model")
    SEO_KEYWORD_INPUT = (By.CSS_SELECTOR, "#input-keyword-0-1, #input-keyword, input[name^='product_seo_url']")
    PRODUCT_ROWS = (By.CSS_SELECTOR, "#form-product tbody tr")
    NO_RESULTS_CELL = (By.XPATH, "//form[@id='form-product']//td[normalize-space()='No results!']")
    ROW_CHECKBOX = (By.CSS_SELECTOR, "input[name='selected[]']")

    def __init__(self, driver: WebDriver, base_url: str, user_token: str) -> None:
        super().__init__(driver, base_url)
        self.user_token = user_token

    def _admin_url(self, route: str, **params) -> str:
        query = urlencode({"route": route, "user_token": self.user_token, **params})
        return f"administration/index.php?{query}"

    @allure.step("Open admin product list (page {page})")
    def open_list(self, page: int = 1) -> None:
        self.logger.info("Opening admin product list, page %s", page)
        self.open(self._admin_url("catalog/product", page=page))
        self.wait_until(
            lambda d: d.find_elements(*self.PRODUCT_ROWS) or d.find_elements(*self.NO_RESULTS_CELL)
        )

    @allure.step("Add product: {name}")
    def add_product(self, name: str, model: str) -> str:
        self.logger.info("Adding product: %s (model: %s)", name, model)
        self.open_list()
        self.click(self.ADD_BUTTON)
        self.wait_visible(self.PRODUCT_NAME_INPUT, timeout=15)
        self.type_text(self.PRODUCT_NAME_INPUT, name)
        self.type_text(self.META_TITLE_INPUT, name)
        self.click(self.DATA_TAB)
        self.wait_visible(self.MODEL_INPUT, timeout=10)
        self.type_text(self.MODEL_INPUT, model)
        self._fill_seo_keyword(name)
        self.click(self.SAVE_BUTTON)
        message = self.wait_visible(self.SUCCESS_ALERT, timeout=15).text.strip()
        self.logger.info("Product added: %s", message)
        return message

    def _fill_seo_keyword(self, keyword: str) -> None:
        try:
            self.click(self.SEO_TAB, timeout=3)
            self.type_text(self.SEO_KEYWORD_INPUT, keyword.replace(" ", "-").lower(), timeout=3)
        except TimeoutException:
            self.logger.debug("SEO tab is not available, skipping keyword fill")

    def _product_row_locator(self, name: str) -> tuple[str, str]:
        return (
            By.XPATH,
            f"//form[@id='form-product']//tr[.//td[contains(normalize-space(), '{name}')]]",
        )

    def _filter_by_name(self, name: str) -> None:
        filter_input = (By.CSS_SELECTOR, "#input-name")
        filter_button = (By.ID, "button-filter")
        try:
            self.wait_visible(filter_input, timeout=5)
            self.type_text(filter_input, name, timeout=5)
            self.click(filter_button, timeout=5)
            self.wait_until(
                lambda d: d.find_elements(*self.PRODUCT_ROWS) or d.find_elements(*self.NO_RESULTS_CELL),
                timeout=10,
            )
        except TimeoutException:
            self.logger.debug("Product filter is not available")

    @allure.step("Check if product exists: {name}")
    def product_exists(self, name: str, max_pages: int = 50) -> bool:
        self.open_list()
        self._filter_by_name(name)
        if self.driver.find_elements(*self._product_row_locator(name)):
            self.logger.info("Product found via filter: %s", name)
            return True

        page = 1
        while page <= max_pages:
            self.open_list(page)
            rows_text = " | ".join(
                row.text.replace("\n", " ").strip()
                for row in self.driver.find_elements(*self.PRODUCT_ROWS)
            )
            self.logger.debug("Product list page %s: %s", page, rows_text[:300])
            if name in rows_text or self.driver.find_elements(*self._product_row_locator(name)):
                self.logger.info("Product found: %s", name)
                return True
            if self.driver.find_elements(*self.NO_RESULTS_CELL):
                self.logger.info("Product not found: %s", name)
                return False
            if len(self.driver.find_elements(*self.PRODUCT_ROWS)) < 10:
                self.logger.info("Product not found: %s", name)
                return False
            page += 1
        return False

    @allure.step("Delete product: {name}")
    def delete_product(self, name: str) -> str:
        self.logger.info("Deleting product: %s", name)
        if not self.product_exists(name):
            raise AssertionError(f"Product '{name}' is not present in the admin list")
        row = self.driver.find_element(*self._product_row_locator(name))
        row.find_element(*self.ROW_CHECKBOX).click()
        self.click(self.DELETE_BUTTON)
        self.wait_until(ec.alert_is_present())
        self.driver.switch_to.alert.accept()
        message = self.wait_visible(self.SUCCESS_ALERT).text.strip()
        self.logger.info("Product deleted: %s", message)
        return message

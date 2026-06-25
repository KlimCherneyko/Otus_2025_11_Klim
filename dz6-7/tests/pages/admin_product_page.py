from urllib.parse import urlencode

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

from tests.pages.base_page import BasePage


class AdminProductPage(BasePage):
    ADD_BUTTON = (By.CSS_SELECTOR, "a[data-original-title='Add New']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[data-original-title='Save']")
    DELETE_BUTTON = (By.CSS_SELECTOR, "button[data-original-title='Delete']")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    PRODUCT_NAME_INPUT = (By.ID, "input-name1")
    META_TITLE_INPUT = (By.ID, "input-meta-title1")
    DATA_TAB = (By.CSS_SELECTOR, "a[href='#tab-data']")
    SEO_TAB = (By.CSS_SELECTOR, "a[href='#tab-seo']")
    MODEL_INPUT = (By.ID, "input-model")
    SEO_KEYWORD_INPUT = (By.ID, "input-keyword")
    PRODUCT_ROWS = (By.CSS_SELECTOR, "#form-product tbody tr")
    NO_RESULTS_CELL = (By.XPATH, "//form[@id='form-product']//td[normalize-space()='No results!']")
    ROW_CHECKBOX = (By.CSS_SELECTOR, "input[name='selected[]']")

    def __init__(self, driver: WebDriver, base_url: str, user_token: str) -> None:
        super().__init__(driver, base_url)
        self.user_token = user_token

    def _admin_url(self, route: str, **params) -> str:
        query = urlencode({"route": route, "user_token": self.user_token, **params})
        return f"admin/index.php?{query}"

    def open_list(self, page: int = 1) -> None:
        self.open(self._admin_url("catalog/product", page=page))
        self.wait_until(
            lambda d: d.find_elements(*self.PRODUCT_ROWS) or d.find_elements(*self.NO_RESULTS_CELL)
        )

    def add_product(self, name: str, model: str) -> str:
        self.open_list()
        self.click(self.ADD_BUTTON)
        self.type_text(self.PRODUCT_NAME_INPUT, name)
        self.type_text(self.META_TITLE_INPUT, name)
        self.click(self.DATA_TAB)
        self.type_text(self.MODEL_INPUT, model)
        self._fill_seo_keyword(name)
        self.click(self.SAVE_BUTTON)
        return self.wait_visible(self.SUCCESS_ALERT).text.strip()

    def _fill_seo_keyword(self, keyword: str) -> None:
        try:
            self.click(self.SEO_TAB, timeout=3)
            self.type_text(self.SEO_KEYWORD_INPUT, keyword, timeout=3)
        except TimeoutException:
            pass

    def _product_row_locator(self, name: str) -> tuple[str, str]:
        return (By.XPATH, f"//form[@id='form-product']//tr[td[normalize-space()='{name}']]")

    def product_exists(self, name: str, max_pages: int = 50) -> bool:
        page = 1
        while page <= max_pages:
            self.open_list(page)
            if self.driver.find_elements(*self._product_row_locator(name)):
                return True
            if self.driver.find_elements(*self.NO_RESULTS_CELL):
                return False
            if len(self.driver.find_elements(*self.PRODUCT_ROWS)) < 10:
                return False
            page += 1
        return False

    def delete_product(self, name: str) -> str:
        if not self.product_exists(name):
            raise AssertionError(f"Product '{name}' is not present in the admin list")
        row = self.driver.find_element(*self._product_row_locator(name))
        row.find_element(*self.ROW_CHECKBOX).click()
        self.click(self.DELETE_BUTTON)
        self.wait_until(ec.alert_is_present())
        self.driver.switch_to.alert.accept()
        return self.wait_visible(self.SUCCESS_ALERT).text.strip()

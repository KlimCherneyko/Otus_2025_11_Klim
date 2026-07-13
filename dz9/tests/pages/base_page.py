import logging
from urllib.parse import urljoin

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    CURRENCY_BUTTON = (By.CSS_SELECTOR, "#form-currency .dropdown-toggle")
    PRICE_VALUES: tuple[str, str] | None = None

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/") + "/"
        self.logger = logging.getLogger(self.__class__.__name__)

    @allure.step("Open page: {path}")
    def open(self, path: str = "") -> None:
        url = urljoin(self.base_url, path)
        self.logger.info("Opening page: %s", url)
        self.driver.get(url)

    @staticmethod
    def _currency_option_locator(currency_title: str) -> tuple[str, str]:
        return (
            By.XPATH,
            f"//form[@id='form-currency']//button[contains(normalize-space(), '{currency_title}')]",
        )

    @allure.step("Switch currency to {currency_title}")
    def switch_currency(self, currency_title: str) -> None:
        self.logger.info("Switching currency to: %s", currency_title)
        self.click(self.CURRENCY_BUTTON)
        self.click(self._currency_option_locator(currency_title))

    def get_prices_text(self) -> list[str]:
        if self.PRICE_VALUES is None:
            raise AssertionError(f"{self.__class__.__name__} does not define PRICE_VALUES locator")
        return self.get_elements_text(self.PRICE_VALUES)

    @allure.step("Switch currency to {currency_title} and wait for price update")
    def switch_currency_and_get_updated_prices(self, currency_title: str) -> tuple[list[str], list[str]]:
        initial_prices = self.get_prices_text()
        self.logger.info("Initial prices: %s", initial_prices)
        self.switch_currency(currency_title)
        self.wait_until(lambda d: self.get_prices_text() != initial_prices)
        updated_prices = self.get_prices_text()
        self.logger.info("Updated prices: %s", updated_prices)
        return initial_prices, updated_prices

    def wait_visible(self, locator: tuple[str, str], timeout: int = 10):
        self.logger.debug("Waiting for visibility: %s", locator)
        return WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(locator))

    @allure.step("Wait for element to be clickable: {locator}")
    def wait_clickable(self, locator: tuple[str, str], timeout: int = 10):
        self.logger.debug("Waiting for clickability: %s", locator)
        return WebDriverWait(self.driver, timeout).until(ec.element_to_be_clickable(locator))

    def wait_all_visible(self, locator: tuple[str, str], timeout: int = 10):
        self.logger.debug("Waiting for all elements visibility: %s", locator)
        return WebDriverWait(self.driver, timeout).until(ec.visibility_of_all_elements_located(locator))

    @allure.step("Click element: {locator}")
    def click(self, locator: tuple[str, str], timeout: int = 10) -> None:
        self.logger.info("Clicking element: %s", locator)
        self.wait_clickable(locator, timeout).click()

    @allure.step("Type text into element: {locator}")
    def type_text(self, locator: tuple[str, str], value: str, timeout: int = 10) -> None:
        self.logger.info("Typing into %s", locator)
        element = self.wait_visible(locator, timeout)
        element.clear()
        element.send_keys(value)

    def wait_until(self, condition, timeout: int = 10):
        self.logger.debug("Waiting for custom condition (timeout=%s)", timeout)
        return WebDriverWait(self.driver, timeout).until(condition)

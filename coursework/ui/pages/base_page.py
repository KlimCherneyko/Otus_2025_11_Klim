import logging
from urllib.parse import urljoin

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/") + "/"
        self.logger = logging.getLogger(self.__class__.__name__)

    @allure.step("Open page: {path}")
    def open(self, path: str = "") -> None:
        url = urljoin(self.base_url, path)
        self.logger.info("Opening page: %s", url)
        self.driver.get(url)

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

    def wait_until(self, condition, timeout: int = 10):
        self.logger.debug("Waiting for custom condition (timeout=%s)", timeout)
        return WebDriverWait(self.driver, timeout).until(condition)

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

    def get_text(self, locator: tuple[str, str], timeout: int = 10) -> str:
        return self.wait_visible(locator, timeout).text

    def get_elements_text(self, locator: tuple[str, str]) -> list[str]:
        return [element.text for element in self.wait_all_visible(locator)]

    def find_all(self, locator: tuple[str, str]):
        return self.driver.find_elements(*locator)

    def is_displayed(self, locator: tuple[str, str]) -> bool:
        elements = self.find_all(locator)
        return bool(elements) and elements[0].is_displayed()

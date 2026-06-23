from urllib.parse import urljoin

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/") + "/"

    def open(self, path: str = "") -> None:
        self.driver.get(urljoin(self.base_url, path))

    def wait_visible(self, locator: tuple[str, str], timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(locator))

    def wait_clickable(self, locator: tuple[str, str], timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(ec.element_to_be_clickable(locator))

    def wait_all_visible(self, locator: tuple[str, str], timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(ec.visibility_of_all_elements_located(locator))

    def click(self, locator: tuple[str, str], timeout: int = 10) -> None:
        self.wait_clickable(locator, timeout).click()

    def type_text(self, locator: tuple[str, str], value: str, timeout: int = 10) -> None:
        element = self.wait_visible(locator, timeout)
        element.clear()
        element.send_keys(value)

    def wait_until(self, condition, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(condition)

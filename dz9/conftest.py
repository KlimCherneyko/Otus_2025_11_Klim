import logging
import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from tests.pages.admin_login_page import AdminLoginPage


def pytest_configure(config: pytest.Config) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        force=True,
    )


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--selenium-browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox"],
        help="Browser for selenium tests: chrome or firefox",
    )
    parser.addoption(
        "--opencart-url",
        action="store",
        default="https://opencart.abstracta.us/",
        help="Base URL for OpenCart tests",
    )
    parser.addoption(
        "--selenium-headed",
        action="store_true",
        default=False,
        help="Run Selenium browser with visible UI (disable headless mode)",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            try:
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as exc:
                logging.getLogger(__name__).warning("Failed to capture screenshot: %s", exc)


@pytest.fixture(scope="session")
def base_url(request: pytest.FixtureRequest) -> str:
    return request.config.getoption("--opencart-url")


def _resolve_chrome_paths() -> tuple[str | None, str | None]:
    chrome_bin = os.getenv("CHROME_BIN")
    chromedriver_path = os.getenv("CHROMEDRIVER_PATH")

    for candidate in (chrome_bin, "/usr/bin/chromium", "/usr/bin/google-chrome"):
        if candidate and os.path.isfile(candidate):
            chrome_bin = candidate
            break
    else:
        chrome_bin = None

    for candidate in (chromedriver_path, "/usr/bin/chromedriver"):
        if candidate and os.path.isfile(candidate):
            chromedriver_path = candidate
            break
    else:
        chromedriver_path = None

    return chrome_bin, chromedriver_path


@pytest.fixture()
def driver(request: pytest.FixtureRequest):
    browser_name = request.config.getoption("--selenium-browser")
    headed_mode = request.config.getoption("--selenium-headed")
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.page_load_strategy = "eager"
        options.add_argument("--window-size=1920,1080")
        if not headed_mode:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        chrome_bin, chromedriver_path = _resolve_chrome_paths()
        if chrome_bin:
            options.binary_location = chrome_bin

        if chromedriver_path:
            web_driver = webdriver.Chrome(
                service=ChromeService(chromedriver_path),
                options=options,
            )
        else:
            try:
                web_driver = webdriver.Chrome(options=options)
            except Exception as exc:
                if "Unable to obtain driver" not in str(exc):
                    raise
                from webdriver_manager.chrome import ChromeDriverManager

                web_driver = webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=options,
                )
    else:
        options = webdriver.FirefoxOptions()
        options.page_load_strategy = "eager"
        if not headed_mode:
            options.add_argument("--headless")
        try:
            web_driver = webdriver.Firefox(options=options)
        except Exception as exc:
            if "Unable to obtain driver" not in str(exc):
                raise
            from webdriver_manager.firefox import GeckoDriverManager

            web_driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options,
            )
        web_driver.set_window_size(1920, 1080)

    web_driver.set_page_load_timeout(60)
    web_driver.set_script_timeout(30)

    yield web_driver
    web_driver.quit()


@pytest.fixture()
def admin_credentials() -> tuple[str, str]:
    username = os.getenv("OPENCART_ADMIN_USER")
    password = os.getenv("OPENCART_ADMIN_PASSWORD")
    if not username or not password:
        pytest.skip("Set OPENCART_ADMIN_USER and OPENCART_ADMIN_PASSWORD to run admin scenarios")
    return username, password


@pytest.fixture()
def admin_session(driver, base_url: str, admin_credentials: tuple[str, str]) -> AdminLoginPage:
    username, password = admin_credentials
    login_page = AdminLoginPage(driver, base_url)
    login_page.open()
    login_page.login(username, password)
    login_page.wait_for_dashboard()

    yield login_page

    try:
        login_page.logout()
    except Exception:
        pass

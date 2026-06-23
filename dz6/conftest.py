import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


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


@pytest.fixture(scope="session")
def base_url(request: pytest.FixtureRequest) -> str:
    return request.config.getoption("--opencart-url")


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

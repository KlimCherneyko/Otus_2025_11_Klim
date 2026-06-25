from tests.pages.admin_login_page import AdminLoginPage
from tests.pages.catalog_page import CatalogPage
from tests.pages.main_page import MainPage
from tests.pages.product_page import ProductPage
from tests.pages.registration_page import RegistrationPage


def test_main_page_elements_presence(driver, base_url):
    page = MainPage(driver, base_url)
    page.open()

    for locator in [
        page.LOGO,
        page.SEARCH_INPUT,
        page.NAVBAR_MENU,
        page.CURRENCY_BUTTON,
        page.CART_BUTTON,
    ]:
        page.wait_visible(locator)


def test_catalog_page_elements_presence(driver, base_url):
    page = CatalogPage(driver, base_url)
    page.open()

    for locator in [
        page.PAGE_TITLE,
        page.BREADCRUMB,
        page.SORT_SELECT,
        page.LIMIT_SELECT,
        page.CURRENCY_BUTTON,
    ]:
        page.wait_visible(locator)


def test_product_page_elements_presence(driver, base_url):
    page = ProductPage(driver, base_url)
    page.open()

    for locator in [
        page.PAGE_TITLE,
        page.MAIN_IMAGE,
        page.PRICE_BLOCK,
        page.QUANTITY_INPUT,
        page.ADD_TO_CART_BUTTON,
    ]:
        page.wait_visible(locator)


def test_admin_login_page_elements_presence(driver, base_url):
    page = AdminLoginPage(driver, base_url)
    page.open()

    for locator in [
        page.PAGE_TITLE,
        page.USERNAME_INPUT,
        page.PASSWORD_INPUT,
        page.LOGIN_BUTTON,
        page.FORGOTTEN_PASSWORD_LINK,
    ]:
        page.wait_visible(locator)


def test_registration_page_elements_presence(driver, base_url):
    page = RegistrationPage(driver, base_url)
    page.open()

    for locator in [
        page.PAGE_TITLE,
        page.FIRST_NAME_INPUT,
        page.LAST_NAME_INPUT,
        page.EMAIL_INPUT,
        page.CONTINUE_BUTTON,
    ]:
        page.wait_visible(locator)

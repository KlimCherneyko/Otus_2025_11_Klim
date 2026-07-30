import os
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.common import AppiumOptions
from selenium.webdriver.remote.command import Command

APK_PATH = (
    Path(__file__).resolve().parent.parent
    / "домашка-файлы"
    / "pnv_486875_ece65f-582630-edb363.apk"
)
APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")

options = AppiumOptions()
options.load_capabilities(
    {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:app": str(APK_PATH),
    }
)


class ReportCommand(Command):
    GET_REPORT: str = "getReport"
    DELETE_REPORT: str = "deleteReport"
    SET_TEST_INFO: str = "setTestInfo"


@pytest.fixture()
def driver():
    android_driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
    android_driver.command_executor._commands = {
        **android_driver.command_executor._commands,
        ReportCommand.GET_REPORT: ("GET", "/getReport"),
        ReportCommand.DELETE_REPORT: ("DELETE", "/deleteReportData"),
        ReportCommand.SET_TEST_INFO: ("POST", "/setTestInfo"),
    }
    android_driver.execute(ReportCommand.DELETE_REPORT)
    yield android_driver
    android_driver.quit()


@pytest.fixture()
def report(driver, request):
    yield
    test_name = request.node.name
    marker = request.node.get_closest_marker("status")
    raw_status = marker.kwargs.get("status", "unknown") if marker else "unknown"
    status_map = {
        "passed": "PASSED",
        "failed": "FAILED",
        "skipped": "PENDING",
    }
    test_status = status_map.get(str(raw_status).lower(), str(raw_status).upper())

    driver.execute(
        ReportCommand.SET_TEST_INFO,
        {
            "sessionId": driver.session_id,
            "testName": test_name,
            "testStatus": test_status,
        },
    )
    html = driver.execute(ReportCommand.GET_REPORT)
    report_path = Path(__file__).resolve().parent / "report.html"
    with open(report_path, "wt", encoding="utf-8") as r:
        r.write(html["value"])


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        item.add_marker(pytest.mark.status(status=rep.outcome))

import os
import allure
import pytest
from playwright.sync_api import sync_playwright


def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="Run headed browser")
    parser.addoption("--browser", action="store", default="chromium", help="chromium|firefox|webkit")


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://www.saucedemo.com/")


@pytest.fixture()
def page(request):
    headed = request.config.getoption("--headed")
    browser_name = request.config.getoption("--browser")

    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=not headed)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        yield page

        # на падении - скриншот в Allure
        try:
            if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
                png = page.screenshot(full_page=True)
                allure.attach(png, name="screenshot", attachment_type=allure.attachment_type.PNG)
        finally:
            context.close()
            browser.close()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        item.rep_call = rep

import re
import allure
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page, base_url: str = ""):
        self.page = page
        self.base_url = base_url.rstrip("/") if base_url else ""

    @allure.step("Открыть страницу: {path}")
    def open(self, path: str = ""):
        if not self.base_url:
            raise ValueError("base_url пустой.")
        url = f"{self.base_url}{path}"
        self.page.goto(url)

    @allure.step("Проверить содрежит ли URL : {expected_part}")
    def assert_url_contains(self, expected_part: str, timeout: int = 5000):
        expect(self.page).to_have_url(re.compile(rf".*{re.escape(expected_part)}.*"), timeout=timeout)

    @allure.step("Проверить равен ли URL: {expected_path}")
    def assert_url_path(self, expected_path: str, timeout: int = 5000):
        if not self.base_url:
            raise ValueError("base_url пустой.")
        expect(self.page).to_have_url(f"{self.base_url}{expected_path}", timeout=timeout)

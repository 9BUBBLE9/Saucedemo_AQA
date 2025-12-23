import allure
from playwright.sync_api import expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/"

    def __init__(self, page, base_url: str):
        super().__init__(page, base_url)
        self.username = page.locator("[data-test='username']")
        self.password = page.locator("[data-test='password']")
        self.login_btn = page.locator("[data-test='login-button']")
        self.error = page.locator("[data-test='error']")
        self.form = page.locator(".login_wrapper")

    @allure.step("Открыть страницу логина")
    def open(self):
        super().open(self.PATH)
        
    @allure.step("Проверка что мы на странице логина")
    def assert_opened(self):
        self.assert_url_path(self.PATH)
        expect(self.form).to_be_visible()

    @allure.step("Проверка, что форма логина видима")
    def assert_form_visible(self):
        expect(self.form).to_be_visible()

    @allure.step("Выполнить логин: {username}")
    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_btn.click()

    @allure.step("Проверка текста ошибки: {text}")
    def assert_error(self, text: str):
        expect(self.error).to_be_visible()
        expect(self.error).to_contain_text(text)

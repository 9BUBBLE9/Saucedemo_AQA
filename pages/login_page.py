import allure
from playwright.sync_api import Page, expect


class LoginPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_box = page.locator("[data-test='error']")

    @allure.step("Открыть страницу логина")
    def open(self):
        self.page.goto(self.URL, wait_until="domcontentloaded")
        expect(self.page).to_have_url(self.URL)

    @allure.step("Заполнить логин: {username}, пароль: {password}")
    def fill_credentials(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)

    @allure.step("Нажать кнопку Login")
    def submit(self):
        self.login_button.click()

    @allure.step("Логин: {username} / {password}")
    def login(self, username: str, password: str):
        self.fill_credentials(username, password)
        self.submit()

    @allure.step("Проверить видимость элементов формы логина")
    def assert_form_visible(self):
        expect(self.username).to_be_visible()
        expect(self.password).to_be_visible()
        expect(self.login_button).to_be_visible()

    @allure.step("Проверить текст ошибки: {expected_text}")
    def assert_error_contains(self, expected_text: str):
        expect(self.error_box).to_be_visible()
        expect(self.error_box).to_contain_text(expected_text)

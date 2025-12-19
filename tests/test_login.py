import allure
import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

import re


@allure.feature("Login")
class TestLogin:
    @allure.title("Успешный логин (standard_user / secret_sauce)")
    def test_login_success(self, page, base_url):
        login = LoginPage(page)
        inventory = InventoryPage(page)

        login.open()
        login.assert_form_visible()

        login.login("standard_user", "secret_sauce")

        # URL + элементы
        inventory.assert_opened()

    @allure.title("Логин с неверным паролем")
    def test_login_wrong_password(self, page):
        login = LoginPage(page)

        login.open()
        login.login("standard_user", "wrong_password")

        login.assert_error_contains("Username and password do not match")

        # на странице логина
        expect(page).to_have_url(LoginPage.URL)

    @allure.title("Логин заблокированного пользователя (locked_out_user)")
    def test_login_locked_out_user(self, page):
        login = LoginPage(page)

        login.open()
        login.login("locked_out_user", "secret_sauce")

        login.assert_error_contains("Sorry, this user has been locked out")

        expect(page).to_have_url(LoginPage.URL)

    @allure.title("Логин с пустыми полями")
    @pytest.mark.parametrize(
        "username,password,expected_error",
        [
            ("", "", "Username is required"),
            ("standard_user", "", "Password is required"),
        ],
        ids=[
            "empty username and password",
            "empty password",
        ]
    )

    def test_login_empty_fields(self, page, username, password, expected_error):
        login = LoginPage(page)

        login.open()
        login.login(username, password)

        login.assert_error_contains(expected_error)
        expect(page).to_have_url(LoginPage.URL)

    @allure.title("performance_glitch_user / корректный переход несмотря на задержки")
    def test_login_performance_glitch_user(self, page):
        login = LoginPage(page)
        inventory = InventoryPage(page)

        login.open()
        login.login("performance_glitch_user", "secret_sauce")

        # у glitch_user может быть задержка
        expect(page).to_have_url(re.compile(r".*/inventory\.html.*"), timeout=20000)
        inventory.assert_opened()

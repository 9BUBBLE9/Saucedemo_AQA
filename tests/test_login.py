import re
import allure
import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


pytestmark = [pytest.mark.login]


@allure.feature("Login")
class TestLogin:

    @allure.title("Успешный логин (standard_user / secret_sauce)")
    @pytest.mark.smoke
    def test_login_success(self, page, base_url):
        login = LoginPage(page, base_url)
        inventory = InventoryPage(page, base_url)

        login.open()
        login.assert_form_visible()
        login.login("standard_user", "secret_sauce")

        inventory.assert_opened()

    @allure.title("Логин с неверным паролем")
    @pytest.mark.negative
    @pytest.mark.regression 
    def test_login_wrong_password(self, page, base_url):
        login = LoginPage(page, base_url)

        login.open()
        login.login("standard_user", "wrong_password")

        login.assert_error("Username and password do not match")
        login.assert_opened()  # вместо expect(page).to_have_url(LoginPage.URL)

    @allure.title("Логин заблокированного пользователя (locked_out_user)")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_login_locked_out_user(self, page, base_url):
        login = LoginPage(page, base_url)

        login.open()
        login.login("locked_out_user", "secret_sauce")

        login.assert_error("Sorry, this user has been locked out.")
        login.assert_opened()

    @allure.title("Логин с пустыми полями")
    @pytest.mark.negative
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "username,password,expected_error",
        [
            ("", "", "Username is required"),
            ("standard_user", "", "Password is required"),
        ],
        ids=[
            "empty username and password",
            "empty password",
        ],
    )
    def test_login_empty_fields(self, page, base_url, username, password, expected_error):
        login = LoginPage(page, base_url)

        login.open()
        login.login(username, password)

        login.assert_error(expected_error)
        login.assert_opened()

    @allure.title("performance_glitch_user - корректный переход несмотря на задержки")
    @pytest.mark.regression
    @pytest.mark.slow
    def test_login_performance_glitch_user(self, page, base_url):
        login = LoginPage(page, base_url)
        inventory = InventoryPage(page, base_url)

        login.open()
        login.login("performance_glitch_user", "secret_sauce")

        # пусть InventoryPage сам проверяет URL/элементы
        expect(page).to_have_url(re.compile(r".*/inventory\.html.*"), timeout=20000)
        inventory.assert_opened()

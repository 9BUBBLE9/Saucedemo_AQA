import allure
from playwright.sync_api import expect
from pages.base_page import BasePage


class InventoryPage(BasePage):
    PATH = "/inventory.html"

    def __init__(self, page, base_url: str):
        super().__init__(page, base_url)
        self.inventory_container = page.locator("[data-test='inventory-container']")
        self.products = page.locator(".inventory_item")

    @allure.step("Проверка что мы на Inventory странице")
    def assert_opened(self):
        self.assert_url_contains(self.PATH)
        expect(self.inventory_container).to_have_count(1)
        expect(self.inventory_container).to_be_visible()
        expect(self.products.first).to_be_visible()

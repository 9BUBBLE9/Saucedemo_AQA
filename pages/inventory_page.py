import re
import allure
from playwright.sync_api import Page, expect


class InventoryPage:
    URL_PART = "/inventory.html"

    def __init__(self, page: Page):
        self.page = page
        self.inventory_container = page.locator("[data-test='inventory-container']")
        self.products = page.locator(".inventory_item")

    @allure.step("Проверка что мы на Inventory странице")
    def assert_opened(self):
        expect(self.page).to_have_url(re.compile(r".*/inventory\.html.*"))
        expect(self.inventory_container).to_have_count(1)
        expect(self.inventory_container).to_be_visible()
        expect(self.products.first).to_be_visible()

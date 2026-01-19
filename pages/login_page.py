"""登录操作页"""
from data.locators import LoginPageLocators
from pages.base_page import BasePage
from playwright.sync_api import Page


class LoginPage(BasePage):
    def __init__(self, page:Page):
        super().__init__(page)
        self.locator = LoginPageLocators()
        self.username = self.get_by_role("textbox", name=self.locator.inputUsername)
        self.pd = self.get_by_role("textbox", name=self.locator.inputPassword)
        self.button_login = self.get_by_role("button", name=self.locator.buttonLogin)

    def login(self, username, password):
        self.fill(self.username, username)
        self.fill(self.pd, password)
        self.click(self.button_login)
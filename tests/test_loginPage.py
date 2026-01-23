"""登录页测试用例"""
from playwright.sync_api import sync_playwright, Page
import pytest

from data.test_datas import valid_login, invalid_login
from pages.login_page import LoginPage
from config.settings import ServerConfig



class TestLoginPage:
    """登录用例"""
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置条件"""
        self.page = page
        self.login_page = LoginPage(page)


    def test_login_page(self, page: Page, server_url):  # 使用 fixture 里的传入的 URL
        """登录成功测试用例"""
        self.login_page.goto(server_url)
        self.login_page.login(valid_login.username, valid_login.password)

        # 断言
        self.login_page.assert_text_visible("首页")

    def test_login_page_error(self, page: Page, server_url):
        """登录失败测试用例"""
        self.login_page.goto(server_url)
        self.login_page.login(invalid_login.username, invalid_login.password)

        # 断言
        self.login_page.assert_text_visible("用户或密码错误")


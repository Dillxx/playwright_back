"""登录页测试用例"""
from playwright.sync_api import sync_playwright, Page
import pytest

from data.test_datas import valid_login
from pages.login_page import LoginPage
from config.settings import ServerConfig



class TestLoginPage:
    """登录用例"""
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置条件"""
        self.page = page
        self.login_page = LoginPage(page)


    def test_login_page(self, page: Page):
        """登录成功测试用例"""
        self.login_page.goto(ServerConfig.BASE_URL)
        self.login_page.login(valid_login.username, valid_login.password)

        # 断言
        self.login_page.assert_text_visible("首页")


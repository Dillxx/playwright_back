import pytest
from playwright.sync_api import Page
from pages.publicBusiness_page import BusinessPage
from data.test_datas import valid_login
from pages.login_page import LoginPage


class TestBusinessPage:

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.pub_page = BusinessPage(page)
        self.login_page = LoginPage(page)

    def test_publish_steel_cargo(self, page: Page, server_url):
        """测试发布钢铁货源"""
        # 登录
        self.login_page.goto(server_url)
        self.login_page.login(valid_login.username, valid_login.password)

        # 断言
        self.login_page.assert_text_visible("首页")

        # 方式二：调用聚合业务方法（适合集成测试）
        self.pub_page.publish_cargo()

        # 断言结果（假设提交后会跳转或显示成功提示）
        self.pub_page.assert_text_visible("货源创建成功")

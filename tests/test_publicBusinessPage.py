import pytest
from playwright.sync_api import Page
from pages.publicBusiness_page import BusinessPage
from data.test_datas import valid_login
from pages.login_page import LoginPage


class TestBusinessPage:

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.pub_page = BusinessPage(page)

    def test_publish_steel_cargo(self, page: Page, server_url):
        """测试发布钢铁货源"""

        # 导航网址
        page.goto(server_url + "/home")

        self.pub_page.publish_cargo()

        # 断言结果（假设提交后会跳转或显示成功提示）
        self.pub_page.assert_text_visible("货源创建成功")

    def test_publish_steel_cargo_error(self, page: Page, server_url):
        """测试发布钢铁货源:货物价值为空"""

        # 导航网址
        page.goto(server_url + "/home")

        # 方式二：调用聚合业务方法（适合集成测试）
        # 校验货物价值是否必填：可选 None 或 “”，二者区别：“” 可进入输入框执行操作，None 直接跳过输入操作。“” 更符合必填项校验
        self.pub_page.publish_cargo(goodsValue="")
        # self.pub_page.publish_cargo(goodsValue=None)

        # 断言结果（假设提交后会跳转或显示成功提示）
        self.pub_page.assert_text_visible("货物价值不能为空")

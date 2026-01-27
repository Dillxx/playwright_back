import pytest
from playwright.sync_api import Page
from pages.publicBusiness_page import BusinessPage
from data.test_datas import valid_login
from pages.login_page import LoginPage
from utils.read_data import get_csv_data


class TestBusinessPage:

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.pub_page = BusinessPage(page)

    @pytest.mark.business
    @pytest.mark.p0
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

    @pytest.mark.business
    @pytest.mark.p1
    @pytest.mark.parametrize("data", get_csv_data("cargo_data.csv"))
    def test_data_driver(self, page: Page, server_url, data):
        """数据驱动/参数化：测试发布钢铁货源"""

        # 导航网址
        page.goto(server_url + "/home")

        self.pub_page.publish_cargo(
            goodType=data["goodType"],
            quantityGoods=data["quantityGoods"],
            deliveryMethod=data["deliveryMethod"],
            deliveryMethod2=data["deliveryMethod2"],
            startTime=data["startTime"],
            endTime=data["endTime"],
            goodsValue=data["goodsValue"],
            pickingUnitContent=data["pickingUnitContent"],
            receivingUnitContent=data["receivingUnitContent"]
        )

        # 断言结果（假设提交后会跳转或显示成功提示）
        self.pub_page.assert_text_visible(data["expected"])

from pages.base_page import BasePage
from playwright.sync_api import Page
from data.locators import BusinessPageLocators


class BusinessPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.locator = BusinessPageLocators()

    """===============操作层==================="""

    @property           # 使用 property 装饰器作用：调用函数 可以像 访问变量 一样。注意：调用是不能加括号
    def get_BCenter(self):
        """获取业务中心元素"""
        return self.get_by_text(self.locator.BCenter)

    @property
    def get_SourceManagement(self):
        """获取货源管理元素"""
        return self.get_by_text(self.locator.SourceManagement)

    @property
    def get_ReleaseSource(self):
        """获取发布货源元素"""
        return self.get_by_role("button", name=self.locator.ReleaseSource)

    @property
    def get_Good(self):
        """获取货品元素"""
        return self.get_by_text(self.locator.Good)

    @property
    def get_GoodType(self):
        """获取货品名元素"""
        return self.get_by_text(self.locator.GoodType)

    @property
    def get_QuantityGoods(self):
        """获取货物量元素"""
        return self.get_by_role("textbox", name=self.locator.QuantityGoods)

    @property
    def get_ShippingMType(self):
        """获取发货方式元素"""
        return self.get_by_text(self.locator.ShippingMType)

    @property
    def get_DeliveryMethod(self):
        """获取发货对象内容元素"""
        return self.get_by_role("option", name=self.locator.DeliveryMethod)

    @property
    def get_DeliveryMethod2(self):
        """获取发货对象内容 2元素"""
        return self.get_by_text(self.locator.DeliveryMethod2)

    @property
    def get_LoadingTime(self):
        """获取装货时间元素"""
        return self.get_by_role("textbox", name=self.locator.LoadingTime)

    @property
    def get_StartTime(self):
        """获取装货开始时间元素"""
        return self.get_by_text(self.locator.StartTime)

    @property
    def get_EndTime(self):
        """获取装货结束时间元素"""
        return self.get_by_text(self.locator.EndTime)

    @property
    def get_GoodsValue(self):
        """获取货物价值元素"""
        return self.get_by_role("textbox", name=self.locator.GoodsValue)

    @property
    def get_PickingUnit(self):
        """获取提货单位元素"""
        return self.get_by_text(self.locator.PickingUnit)

    @property
    def get_PickingUnitContent(self):
        """获取提货单位地址元素"""
        return self.get_by_text(self.locator.PickingUnitContent)

    @property
    def get_ReceivingUnit(self):
        """获取收货单位元素"""
        return self.get_by_text(self.locator.ReceivingUnit)

    @property
    def get_ReceivingUnitContent(self):
        """获取收货单位地址元素"""
        return self.get_by_text(self.locator.ReceivingUnitContent)

    @property
    def get_Agree(self):
        """获取合同单选框元素"""
        return self.get_by_role("checkbox", name=self.locator.Agree)

    @property
    def get_Submit(self):
        """获取提交元素"""
        return self.get_by_role("button", name=self.locator.Submit)

    """===============操作层==================="""
    def navigate_to_publish_page(self) ->None:
        """进入发布货源页面"""
        self.click(self.get_BCenter)
        self.click(self.get_SourceManagement)
        self.click(self.get_ReleaseSource)

    def fill_cargo_basic_info(self, quantityGoods: str) -> None:
        """填写基础信息"""
        self.click(self.get_Good)
        self.click(self.get_GoodType)
        self.fill(self.get_QuantityGoods, quantityGoods)
        self.click(self.get_ShippingMType.first)
        self.click(self.get_DeliveryMethod)
        self.click(self.get_ShippingMType.nth(1))
        self.click(self.get_DeliveryMethod2)

    def fill_shipping_info(self, goodsValue: str) -> None:
        """填写运输要求"""
        self.click(self.get_LoadingTime)
        self.click(self.get_StartTime.nth(1))
        self.click(self.get_EndTime.first)
        self.fill(self.get_GoodsValue, goodsValue)

    def fill_address_info(self) -> None:
        """填写提收货信息"""
        self.click(self.get_PickingUnit)
        self.click(self.get_PickingUnitContent)
        self.click(self.get_ReceivingUnit)
        self.click(self.get_ReceivingUnitContent)

    def submit_form(self) -> None:
        """勾选协议并提交"""
        self.check(self.get_Agree)
        self.click(self.get_Submit)

    """===============业务层==================="""
    def publish_cargo(self, quantityGoods="500", goodsValue="30") -> None:
        """完整的发布货源流程"""
        self.navigate_to_publish_page()
        self.fill_cargo_basic_info(quantityGoods)
        self.fill_shipping_info(goodsValue)
        self.fill_address_info()
        self.submit_form()


















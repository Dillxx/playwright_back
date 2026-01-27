from pages.base_page import BasePage
from playwright.sync_api import Page
from data.locators import BusinessPageLocators


class BusinessPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.locator = BusinessPageLocators()

    """===============操作层==================="""

    @property           # 使用 property 装饰器作用：调用函数 可以像 访问变量 一样。注意：调用时不能加括号。使用场景：只能在类中使用
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
    def get_QuantityGoods(self):
        """获取货物量元素"""
        return self.get_by_role("textbox", name=self.locator.QuantityGoods)

    @property
    def get_ShippingMType(self):
        """获取发货方式元素"""
        return self.get_by_text(self.locator.ShippingMType)

    @property
    def get_LoadingTime(self):
        """获取装货时间元素"""
        return self.get_by_role("textbox", name=self.locator.LoadingTime)

    @property
    def get_GoodsValue(self):
        """获取货物价值元素"""
        return self.get_by_role("textbox", name=self.locator.GoodsValue)

    @property
    def get_PickingUnit(self):
        """获取提货单位元素"""
        return self.get_by_text(self.locator.PickingUnit)

    @property
    def get_ReceivingUnit(self):
        """获取收货单位元素"""
        return self.get_by_text(self.locator.ReceivingUnit)

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

    def fill_cargo_basic_info(self, goodType: str, quantityGoods: str, deliveryMethod: str, deliveryMethod2: str) -> None:
        """
        goodType: 货品
        quantityGoods：货物数量
        deliveryMethod： 发货对象
        deliveryMethod2： 发货方式
        return: None
        """
        """填写基础信息"""
        self.click(self.get_Good)
        self.click(self.get_by_text(goodType))
        self.fill(self.get_QuantityGoods, quantityGoods)
        self.click(self.get_ShippingMType.first)
        self.click(self.get_by_role("option", name=deliveryMethod))
        self.click(self.get_ShippingMType.nth(1))
        self.click(self.get_by_text(deliveryMethod2))

    def fill_shipping_info(self, startTime: str, endTime: str,  goodsValue: str = None) -> None:
        """
        startTime: 装货开始时间
        endTime： 装货结束时间
        goodsValue： 货物价值
        """
        """填写运输要求"""
        self.click(self.get_LoadingTime)
        self.click(self.get_by_text(startTime).nth(1))
        self.click(self.get_by_text(endTime).first)
        if goodsValue is not None:  # 校验是否为必填操作，其他必填项一样的操作。作用：用于兼容必填项不填的情况
            self.fill(self.get_GoodsValue, goodsValue)

    def fill_address_info(self, pickingUnitContent: str, receivingUnitContent: str) -> None:
        """
        pickingUnitContent：提货地址
        receivingUnitContent：收货地址
        """
        """填写提收货信息"""
        self.click(self.get_PickingUnit)
        self.click(self.get_by_text(pickingUnitContent))
        self.click(self.get_ReceivingUnit)
        self.click(self.get_by_text(receivingUnitContent))

    def submit_form(self) -> None:
        """勾选协议并提交"""
        self.check(self.get_Agree)
        self.click(self.get_Submit)

    """===============业务层==================="""
    def publish_cargo(self, goodType="钢铁",  quantityGoods="500",  deliveryMethod="司机",  deliveryMethod2="指派司机",  startTime="8",  endTime="22", goodsValue="30",  pickingUnitContent="静安路",  receivingUnitContent="祥厚路") -> None:
        """完整的发布货源流程"""
        self.navigate_to_publish_page()
        self.fill_cargo_basic_info(goodType, quantityGoods, deliveryMethod, deliveryMethod2)
        self.fill_shipping_info(startTime, endTime, goodsValue)
        self.fill_address_info(pickingUnitContent, receivingUnitContent)
        self.submit_form()


















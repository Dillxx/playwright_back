# 快速录制命令： python3 -m playwright codegen --target python -o 'test_01' -b chromium  http://dev8.kuotian.cc


import re
from playwright.sync_api import Page, expect


# def test_example(page: Page) -> None:
#     page.goto("http://dev8.kuotian.cc/login")
#     page.get_by_role("textbox", name="请输入登录账号").click()
#     page.get_by_role("textbox", name="请输入登录账号").fill("18888888888")
#     page.get_by_role("textbox", name="请输入登录账号").press("Tab")
#     page.get_by_role("textbox", name="请输入登录密码").fill("Hqq123456")
#     page.get_by_role("button", name="登 录").click()
#     page.locator("div").filter(has_text=re.compile(r"^业务中心$")).click()
#     page.get_by_text("货源管理").click()
#     page.get_by_role("button", name="图标: plus 发布货源").click()
#     page.locator("img").nth(2).click()
#     page.get_by_text("请选择货品").click()
#     page.get_by_text("油").click()
#     page.get_by_role("textbox", name="请输入货物数量(预估)").click()
#     page.get_by_role("textbox", name="请输入货物数量(预估)").fill("200")
#     page.locator("div").filter(has_text=re.compile(r"^请选择发货方式$")).nth(2).click()
#     page.get_by_role("option", name="司机").click()
#     page.get_by_text("请选择发货方式").nth(1).click()
#     page.get_by_text("指派司机").click()
#     page.get_by_role("textbox", name="开始日期").click()
#     page.get_by_text("1").nth(5).click()
#     page.get_by_role("gridcell", name="31").nth(1).click()
#     page.get_by_text("请选择提货单位").click()
#     page.get_by_text("建设路提货点").click()
#     page.get_by_text("请选择收货单位").click()
#     page.get_by_text("祥厚路").click()
#     page.get_by_role("checkbox", name="同意").check()
#     page.get_by_role("button", name="提 交").click()

class testDemo():
    def __init__(self):
        """公共变量"""
        self.url = "http://dev8.kuotian.cc/login"
        self.page = Page

    def setup(self):
        """"初始化操作"""


    def testLogin(self):
        """登录用例：成功登录"""
        self.page.goto(self.url)
        self.page.get_by_role("textbox", name="请输入登录账号").click().fill("18888888888")
        self.page.get_by_role("textbox", name="请输入登录密码").click().fill("Hqq123456")
        self.page.get_by_role("textbox", name="登录").click()

if __name__ == '__main__':
    test01 = testDemo()
    test01.testLogin()
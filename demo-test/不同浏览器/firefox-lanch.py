from playwright.sync_api import sync_playwright

# 上下文管理浏览器生命周期
# with sync_playwright() as p:
#     browser = p.firefox.launch(headless=False)  # 启动 firefox 浏览器
#     page = browser.new_page()  # 打开新页面
#     page.goto('http://dev8.kuotian.cc')  # 访问 dev8网址，登录页
#     page.get_by_role("textbox", name="请输入登录账号").fill("18888888888")
#     page.get_by_role("textbox", name="请输入登录密码").fill("Hqq123456")
#     page.get_by_role("button", name="登 录").click()
#     page.screenshot(path=f'{p.firefox.name}.jpg')  # 截图
#     browser.close()
#
# 手动控制浏览器生命周期
playwright = sync_playwright().start()
browser = playwright.firefox.launch(headless=False, slow_mo=1000)
page = browser.new_page()
page.wait_for_timeout(1000) # 强制等待时间 1s
page.goto("http://dev8.kuotian.cc")
page.get_by_role("textbox", name="请输入登录账号").fill("18888888888")
page.get_by_role("textbox", name="请输入登录密码").fill("Hqq123456")
page.get_by_role("button", name="登 录").click()
page.wait_for_timeout(1000)
page.close()
playwright.stop()

# # 异步处理
# from playwright.async_api import async_playwright  # 异步处理模块
# import asyncio
# import pytest
#
# # @pytest.mark.asyncio
# async  def test_001():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         page = await browser.new_page()
#         await page.goto("http://dev8.kuotian.cc")
#         await page.get_by_role("textbox", name="请输入登录账号").fill("18888888888")
#         await page.get_by_role("textbox", name="请输入登录密码").fill("Hqq123456")
#         await page.get_by_role("button", name="登 录").click()
#         await page.wait_for_timeout(1000)
#         await page.close()
#         print("一致性")


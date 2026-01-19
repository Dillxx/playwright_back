from playwright.sync_api import sync_playwright


playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, slow_mo=1000, args=["--start-maximized"])
context1 = browser.new_context(no_viewport=True)
# context1.add_cookies()
context2 = browser.new_context(no_viewport=True)
page = context1.new_page()
page.wait_for_timeout(1000) # 强制等待时间 1s
page.goto("http://dev8.kuotian.cc")
page.get_by_role("textbox", name="请输入登录账号").fill("18888888888")
page.get_by_role("textbox", name="请输入登录密码").fill("Hqq123456")
page.get_by_role("button", name="登 录").click()
page.wait_for_timeout(1000)
# page.close()

page2 = context2.new_page()
page2.wait_for_timeout(1000) # 强制等待时间 1s
page2.goto("http://dev8.kuotian.cc")
page2.get_by_role("textbox", name="请输入登录账号").fill("18888888888")
page2.get_by_role("textbox", name="请输入登录密码").fill("Hqq123456")
page2.get_by_role("button", name="登 录").click()
page2.wait_for_timeout(1000)
# page2.close()


playwright.stop()
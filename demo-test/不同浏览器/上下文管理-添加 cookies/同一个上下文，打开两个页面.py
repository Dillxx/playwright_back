from playwright.sync_api import sync_playwright


playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, slow_mo=1000, args=["--start-maximized"])
context = browser.new_context(no_viewport=True)
page = context.new_page()
page2 = context.new_page()

page.goto("http://dev8.kuotian.cc")
page.get_by_role("textbox", name="请输入登录账号").fill("18888888888")
page.get_by_role("textbox", name="请输入登录密码").fill("Hqq123456")
page.get_by_role("button", name="登 录").click()
page.wait_for_timeout(1000)

page2.goto("http://dev9.kuotian.cc")
page2.get_by_role("textbox", name="请输入登录账号").fill("17888888888")
page2.get_by_role("textbox", name="请输入登录密码").fill("Hqq123456")
page2.get_by_role("button", name="登 录").click()
page2.wait_for_timeout(1000)


context.close()
playwright.stop()
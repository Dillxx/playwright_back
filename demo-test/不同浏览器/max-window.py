from playwright.sync_api import sync_playwright


playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, slow_mo=1000, args=["--start-maximized"])
page = browser.new_page(no_viewport=True)  # 最大化时，必须设置此参数，否则最大化后会缩小为原比例
page.wait_for_timeout(1000) # 强制等待时间 1s
page.goto("http://dev8.kuotian.cc")
page.get_by_role("textbox", name="请输入登录账号").fill("18888888888")
page.get_by_role("textbox", name="请输入登录密码").fill("Hqq123456")
page.get_by_role("button", name="登 录").click()
page.wait_for_timeout(1000)
page.close()
playwright.stop()
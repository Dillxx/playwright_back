from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=False)  # 启动 chrome 浏览器
    page = browser.new_page()  # 打开新页面
    page.goto('http://dev8.kuotian.cc')  # 访问 dev8网址，登录页
    page.get_by_role("textbox", name="请输入登录账号").fill("18888888888")
    page.get_by_role("textbox", name="请输入登录密码").fill("Hqq123456")
    page.get_by_role("button", name="登 录").click()
    page.screenshot(path=f'{p.chromium.name}.jpg')  # 截图
    browser.close()

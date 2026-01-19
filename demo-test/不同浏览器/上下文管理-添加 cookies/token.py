from playwright.sync_api import sync_playwright

# # 获取 token
# with sync_playwright() as p:
#     # 1. 直接通过 API 请求获取 Token (速度极快，不需要渲染页面)
#     api_request = p.request.new_context(
#         extra_http_headers={
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#             "Content-Type": "application/json"
#         }
#     )
#     response = api_request.post("http://dev8.kuotian.cc/api/login", json={
#         "username": "18888888888",
#         "password": "Hqq123456"
#     })
#     # 假设返回的 json 是 {"data": {"token": "eyJhbGci..."}}
#     token = response.json()["data"]["token"]
#
# print(token)

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, slow_mo=1000, args=["--start-maximized"])
context1 = browser.new_context(no_viewport=True)

# 添加 token
context1.set_extra_http_headers(
    {
        "Token" : "1060875196434481152"
    }
)


page = context1.new_page()
page.wait_for_timeout(1000) # 强制等待时间 1s
page.goto("http://dev8.kuotian.cc/netOrder/goods")
# page.get_by_role("textbox", name="请输入登录账号").fill("18888888888")
# page.get_by_role("textbox", name="请输入登录密码").fill("Hqq123456")
# page.get_by_role("button", name="登 录").click()
page.wait_for_timeout(9000)
page.close()
playwright.stop()

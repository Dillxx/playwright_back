# 3.导入模块
from playwright.sync_api import sync_playwright
#打开两个浏览器上下文
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False,slow_mo=100) #打开浏览器
    context1 = browser.new_context() #创建浏览器上下文，支持创建多个上下文
    page1 = context1.new_page()#新打开一个浏览器标签页
    page1.goto("https://baidu.com")
    context2 = browser.new_context()  # 创建浏览器上下文，支持创建多个上下文
    page2 = context2.new_page()#新打开一个浏览器标签页
    page2.goto("https://www.bilibili.com")
    browser.close()

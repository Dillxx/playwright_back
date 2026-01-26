# """
# Pytest 配置和 fixtures
# """
# import pytest
# from pathlib import Path
# from playwright.sync_api import sync_playwright
# from config.settings import BrowserConfig, ServerConfig, ScreenshotConfig
# from utils.logger import get_logger
#
# logger = get_logger(__name__)
# ScreenshotConfig.ensure_screenshot_dir()
#
#
# @pytest.fixture(scope="session")    # 整个测试过程只执行一次  session 控制
# def browser_config():
#     """浏览器配置 fixture"""
#     return BrowserConfig()
#
#
# @pytest.fixture(scope="function")   # 每个测试用例都需要执行，function 控制
# # def browser():  back
# def browser(browser_config):  # 使用 pytest 的依赖注入功能
#     """浏览器 fixture"""
#     logger.info("启动浏览器")
#     playwright = sync_playwright().start()
#     browser = playwright.chromium.launch(
#         headless=browser_config.HEADLESS,
#         slow_mo=browser_config.SLOW_MO,
#         args=browser_config.Args
#     )
#     yield browser   # 测试结束后，关闭浏览器
#     logger.info("关闭浏览器")
#     browser.close()
#     playwright.stop()
#
#
# @pytest.fixture(scope="function")
# def page(browser):
#     """页面 fixture"""
#     context = browser.new_context(no_viewport=True)
#     page = context.new_page()
#     page.set_default_timeout(BrowserConfig.TIMEOUT)
#
#     yield page
#
#     # 测试失败时截图
#     if hasattr(page, "context"):
#         page.close()
#     context.close()
#
#
# @pytest.fixture(scope="function")
# def server_url():
#     """服务器 URL fixture"""
#     return ServerConfig.BASE_URL
#
#
# # ==================== Hooks ====================
#
# def pytest_configure(config):
#     """Pytest 配置钩子"""
#     logger.info("=" * 50)
#     logger.info("自动化测试开始")
#     logger.info("=" * 50)
#
#
# def pytest_unconfigure(config):
#     """Pytest 清理钩子"""
#     logger.info("=" * 50)
#     logger.info("自动化测试结束")
#     logger.info("=" * 50)
#
#
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     """测试结果报告钩子"""
#     outcome = yield
#     rep = outcome.get_result()
#
#     if rep.failed:
#         logger.error(f"测试失败: {item.name}")
#
#
#
# """
# 用例执行的完整生命周期：
#
#     [开始测试]
#        ⬇️
#        1. 读取 browser_config
#        ⬇️
#        2. browser fixture (Setup): 启动浏览器
#           ⬇️
#           3. page fixture (Setup): 打开新页面
#              ⬇️
#              ----------------------------------
#              |   4. 执行你的测试用例代码 (Test)   |
#              ----------------------------------
#              ⬇️
#           5. Hook (makereport): 偷看一眼结果 (失败了就报错/截图)
#           ⬇️
#        6. page fixture (Teardown): 关闭页面
#        ⬇️
#        7. browser fixture (Teardown): 关闭浏览器
#        ⬇️
#     [结束测试]
#
# """
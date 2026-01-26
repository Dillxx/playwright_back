"""
Pytest 配置和 fixtures
"""
import os
import time

import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright
from config.settings import BrowserConfig, ServerConfig, ScreenshotConfig
from utils.logger import get_logger
import json

STATE_FILE = Path("auth/state.json")  # 登录态存储文件
MAX_AUTH_AGE = 72 * 3600  # 登录态有效期（秒），24小时 = 86400秒
logger = get_logger(__name__)
ScreenshotConfig.ensure_screenshot_dir()


@pytest.fixture(scope="session")  # 整个测试过程只执行一次  session 控制
def browser_config():
    """浏览器配置 fixture"""
    return BrowserConfig()

@pytest.fixture(scope="session")
def server_url():
    """服务器 URL fixture"""
    return ServerConfig.BASE_URL

def is_auth_expired() -> bool:
    """
    判断登录态文件是否过期
    返回 True = 过期或不存在，需要重新登录
    返回 False = 还在有效期内
    """
    if not STATE_FILE.exists():
        logger.info("登录态文件不存在")
        return True

    file_age = time.time() - os.path.getmtime(STATE_FILE)
    if file_age > MAX_AUTH_AGE:
        logger.info(f"登录态文件已存在 {file_age / 3600:.2f} 小时，超过设定的 {MAX_AUTH_AGE / 3600} 小时，判定为过期")
        return True

    logger.info(f"登录态文件有效（已存在 {file_age / 3600:.2f} 小时）")
    return False



@pytest.fixture(scope="session")
def authenticated_context(browser_config, server_url):
    """
    【核心优化】使用 Storage State 持久化登录态
    - 登录态保存到文件 → 重启测试也能复用
    - CI/CD 可以预先生成登录态文件
    - 支持多账号切换（通过不同的 state 文件）
    """
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=browser_config.HEADLESS,
        slow_mo=browser_config.SLOW_MO,
        args=browser_config.Args
    )

    # 判断是否需要重新登录
    if is_auth_expired():
        logger.info("🔄 准备重新登录...")

        # 创建新的浏览器上下文
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # 执行登录流程
        from pages.login_page import LoginPage
        from data.test_datas import valid_login

        login_page = LoginPage(page)
        login_page.goto(server_url + "/login")
        login_page.login(valid_login.username, valid_login.password)
        login_page.assert_text_visible("首页")  # 确保登录成功

        # 保存最新的登录态
        context.storage_state(path=STATE_FILE)
        logger.info(f"✅ 新的登录态已保存至: {STATE_FILE}")
        page.close()
    else:
        logger.info("✅ 使用现有登录态文件")
        context = browser.new_context(storage_state=STATE_FILE, no_viewport=True)

    yield context

    context.close()
    browser.close()
    playwright.stop()


@pytest.fixture(scope="function")
def page(authenticated_context):
    """使用已认证的上下文创建页面"""
    page = authenticated_context.new_page()
    page.set_default_timeout(BrowserConfig.TIMEOUT)
    yield page
    page.close()





# ==================== Hooks ====================

def pytest_configure(config):
    """Pytest 配置钩子"""
    logger.info("=" * 50)
    logger.info("自动化测试开始")
    logger.info("=" * 50)


def pytest_unconfigure(config):
    """Pytest 清理钩子"""
    logger.info("=" * 50)
    logger.info("自动化测试结束")
    logger.info("=" * 50)


# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     """测试结果报告钩子"""
#     outcome = yield
#     rep = outcome.get_result()
#
#     if rep.failed:
#         logger.error(f"测试失败: {item.name}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图"""
    outcome = yield
    rep = outcome.get_result()

    if rep.failed and rep.when == "call":
        page = item.funcargs.get("page")
        if page:
            screenshot_path = os.path.join(
                ScreenshotConfig.SCREENSHOT_DIR,
                f"fail_{item.name}_{int(time.time())}.png"
            )
            page.screenshot(path=screenshot_path, full_page=True)
            logger.error(f"❌ 测试失败: {item.name}，截图: {screenshot_path}")


"""
用例执行的完整生命周期：

    [开始测试]
       ⬇️
       1. 读取 browser_config
       ⬇️
       2. browser fixture (Setup): 启动浏览器
          ⬇️
          3. page fixture (Setup): 打开新页面
             ⬇️
             ----------------------------------
             |   4. 执行你的测试用例代码 (Test)   |
             ----------------------------------
             ⬇️
          5. Hook (makereport): 偷看一眼结果 (失败了就报错/截图)
          ⬇️
       6. page fixture (Teardown): 关闭页面
       ⬇️
       7. browser fixture (Teardown): 关闭浏览器
       ⬇️
    [结束测试]

"""

"""
Pytest 配置和 fixtures
"""
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright
from config.settings import BrowserConfig, ServerConfig, ScreenshotConfig
from utils.logger import get_logger

logger = get_logger(__name__)
ScreenshotConfig.ensure_screenshot_dir()


@pytest.fixture(scope="session")
def browser_config():
    """浏览器配置 fixture"""
    return BrowserConfig()


@pytest.fixture(scope="function")
def browser():
    """浏览器 fixture"""
    logger.info("启动浏览器")
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=BrowserConfig.HEADLESS,
        slow_mo=BrowserConfig.SLOW_MO
    )
    yield browser
    logger.info("关闭浏览器")
    browser.close()
    playwright.stop()


@pytest.fixture(scope="function")
def page(browser):
    """页面 fixture"""
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(BrowserConfig.TIMEOUT)

    yield page

    # 测试失败时截图
    if hasattr(page, "context"):
        page.close()
    context.close()


@pytest.fixture(scope="function")
def server_url():
    """服务器 URL fixture"""
    return ServerConfig.BASE_URL


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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试结果报告钩子"""
    outcome = yield
    rep = outcome.get_result()

    if rep.failed:
        logger.error(f"测试失败: {item.name}")
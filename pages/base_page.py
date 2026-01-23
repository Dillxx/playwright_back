"""
Page Object 基础类
"""
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Tuple
from playwright.sync_api import Page, expect
from config.settings import ScreenshotConfig, BrowserConfig
from utils.logger import get_logger
from utils.retry import retry

logger = get_logger(__name__)
ScreenshotConfig.ensure_screenshot_dir()


class BasePage:
    """所有页面的基类，提供通用操作方法"""

    def __init__(self, page: Page):
        """
        初始化页面对象

        Args:
            page: Playwright Page 对象
        """
        self.page = page
        self.page.set_default_timeout(BrowserConfig.TIMEOUT)
        logger.info(f"初始化页面: {self.__class__.__name__}")

    # ==================== 导航相关 ====================

    def goto(self, url: str) -> None:
        """
        导航到指定 URL

        Args:
            url: 目标 URL，已配置到环境变量中
        """
        try:
            logger.info(f"导航到: {url}")
            self.page.goto(url, wait_until="networkidle")
            logger.info(f"页面加载成功: {url}")
        except Exception as e:
            logger.error(f"导航失败: {url}, 错误: {e}")
            self.take_screenshot(f"goto_failed_{int(time.time())}")
            raise

    def go_back(self) -> None:  # 疑问点解释：返回值是 None，表示只有动作，不负责产出
        """返回上一页"""
        logger.info("返回上一页")
        self.page.go_back()

    def reload(self) -> None:
        """刷新当前页面"""
        logger.info("刷新页面")
        self.page.reload()

    # ==================== 元素定位 ====================

    def get_element(self, selector: str):   # 疑问点解释：selector：str，表示入参值应该为 字符串类型，比如 C++里的：int a, string b
        """
        获取单个元素

        Args:
            selector: CSS 选择器

        Returns:
            Locator 对象
        """
        return self.page.locator(selector)

    def get_by_text(self, text: str, exact: bool = False):  # 疑问点解释：exact 为布尔类型，并默认赋值为 false
        """
        通过文本定位元素

        Args:
            text: 元素文本
            exact: 是否精确匹配，默认不精确匹配
        """
        return self.page.get_by_text(text, exact=exact)

    def get_by_role(self, role: str, **kwargs):
        """
        通过 ARIA 角色定位元素

        Args:
            role: ARIA 角色 (button, textbox, option 等)
            **kwargs: 其他参数 (name, checked 等)
        """
        return self.page.get_by_role(role, **kwargs)

    def get_by_placeholder(self, text: str):
        """通过占位符定位元素"""
        return self.page.get_by_placeholder(text)

    # ==================== 交互操作 ====================

    @retry(max_attempts=3, delay=0.5)   # 重试机制，暂时可不需要
    def click(self, selector: str, timeout: int = 5000, **kwargs) -> None:
        """
        点击元素（带重试）

        Args:
            selector: CSS 选择器或 Locator
            timeout: 超时时间（毫秒）
            **kwargs: 传递给 click() 的其他参数
        """
        try:
            logger.info(f"点击元素: {selector}")
            locator = self._get_locator(selector)
            locator.click(timeout=timeout, **kwargs)
            logger.debug(f"点击成功: {selector}")
        except Exception as e:
            logger.error(f"点击失败: {selector}, 错误: {e}")
            raise

    @retry(max_attempts=3, delay=0.5)  # 重试机制，暂时可不需要
    def fill(self, selector: str, text: str, timeout: int = 5000) -> None:
        """
        填充输入框（带重试）

        Args:
            selector: CSS 选择器或 Locator
            text: 要填充的文本
            timeout: 超时时间（毫秒）
        """
        try:
            logger.info(f"填充输入框: {selector} = {text}")
            locator = self._get_locator(selector)
            locator.fill(text, timeout=timeout)
            logger.debug(f"填充成功: {selector}")
        except Exception as e:
            logger.error(f"填充失败: {selector}, 错误: {e}")
            raise

    def clear_and_fill(self, selector: str, text: str) -> None:
        """
        清空并填充输入框

        Args:
            selector: CSS 选择器或 Locator
            text: 要填充的文本
        """
        logger.info(f"清空并填充: {selector}")
        locator = self._get_locator(selector)
        locator.clear()
        locator.fill(text)

    def check(self, selector: str) -> None:
        """
        勾选复选框

        Args:
            selector: CSS 选择器或 Locator
        """
        logger.info(f"勾选复选框: {selector}")
        locator = self._get_locator(selector)
        if not locator.is_checked():
            locator.check()
        logger.debug(f"勾选成功: {selector}")

    def uncheck(self, selector: str) -> None:
        """
        取消勾选复选框

        Args:
            selector: CSS 选择器或 Locator
        """
        logger.info(f"取消勾选: {selector}")
        locator = self._get_locator(selector)
        if locator.is_checked():
            locator.uncheck()

    def select_option(self, selector: str, value: str = None, label: str = None) -> None:
        """
        选择下拉框选项

        Args:
            selector: CSS 选择器或 Locator
            value: 选项值
            label: 选项标签
        """
        logger.info(f"选择下拉框选项: {selector}, value={value}, label={label}")
        locator = self._get_locator(selector)
        if value:
            locator.select_option(value)
        elif label:
            locator.select_option(label=label)

    # ==================== 获取数据 ====================

    def get_text(self, selector: str) -> str:
        """
        获取元素文本

        Args:
            selector: CSS 选择器或 Locator

        Returns:
            元素文本
        """
        locator = self._get_locator(selector)
        text = locator.text_content()
        logger.debug(f"获取文本: {selector} = {text}")
        return text

    def get_attribute(self, selector: str, attribute: str) -> str:
        """
        获取元素属性

        Args:
            selector: CSS 选择器或 Locator
            attribute: 属性名

        Returns:
            属性值
        """
        locator = self._get_locator(selector)
        value = locator.get_attribute(attribute)
        logger.debug(f"获取属性: {selector}[{attribute}] = {value}")
        return value

    def get_input_value(self, selector: str) -> str:
        """
        获取输入框值

        Args:
            selector: CSS 选择器或 Locator

        Returns:
            输入框值
        """
        locator = self._get_locator(selector)
        value = locator.input_value()
        logger.debug(f"获取输入值: {selector} = {value}")
        return value

    # ==================== 等待相关 ====================

    def wait_for_element(self, selector: str, timeout: int = 5000) -> None:
        """
        等待元素出现

        Args:
            selector: CSS 选择器或 Locator
            timeout: 超时时间（毫秒）
        """
        logger.info(f"等待元素出现: {selector}")
        locator = self._get_locator(selector)
        locator.wait_for(timeout=timeout, state="visible")
        logger.debug(f"元素已出现: {selector}")

    def wait_for_element_hidden(self, selector: str, timeout: int = 5000) -> None:
        """
        等待元素隐藏

        Args:
            selector: CSS 选择器或 Locator
            timeout: 超时时间（毫秒）
        """
        logger.info(f"等待元素隐藏: {selector}")
        locator = self._get_locator(selector) # 把传入的字符串选择器（CSS Selector）转换成一个 Playwright 的 Locator 对象
        locator.wait_for(timeout=timeout, state="hidden")

    def wait_for_page_load(self) -> None:
        """等待页面加载完成"""
        logger.info("等待页面加载完成")
        self.page.wait_for_load_state("networkidle")

    def wait_for_condition(self, condition_func, timeout: int = 5000,
                           check_interval: int = 500) -> None:
        """
        等待条件满足

        Args:
            condition_func: 返回布尔值的函数
            timeout: 超时时间（毫秒）
            check_interval: 检查间隔（毫秒）
        """
        start_time = time.time()
        while True:
            if condition_func():
                logger.debug("条件已满足")
                return

            if (time.time() - start_time) * 1000 > timeout:
                logger.error(f"等待条件超时: {timeout}ms")
                raise TimeoutError(f"条件等待超时: {timeout}ms")

            time.sleep(check_interval / 1000)

    # ==================== 断言相关 ====================

    def assert_text_visible(self, text: str, timeout: int = 5000) -> None:
        """
        断言文本可见

        Args:
            text: 要断言的文本
            timeout: 超时时间（毫秒）
        """
        logger.info(f"断言文本可见: {text}")
        try:
            expect(self.page.get_by_text(text)).to_be_visible(timeout=timeout) # 疑惑点解释：先在页面上获取断言文本，并且可视化，断言成功则通过，断言失败则抛出错误异常，并标记为 failed
            logger.info(f"文本断言成功: {text}")
        except AssertionError as e:
            logger.error(f"文本断言失败: {text}, 错误: {e}")
            raise   # 必须加上抛出异常，测试框架接收到错误，标记该用例为 FAILED

    def assert_element_visible(self, selector: str, timeout: int = 5000) -> None:
        """
        断言元素可见

        Args:
            selector: CSS 选择器或 Locator
            timeout: 超时时间（毫秒）
        """
        logger.info(f"断言元素可见: {selector}")
        try:
            locator = self._get_locator(selector)
            expect(locator).to_be_visible(timeout=timeout)
            logger.info(f"元素可见断言成功: {selector}")
        except AssertionError as e:
            logger.error(f"元素可见断言失败: {selector}, 错误: {e}")
            raise

    def assert_element_hidden(self, selector: str, timeout: int = 5000) -> None:
        """
        断言元素隐藏

        Args:
            selector: CSS 选择器或 Locator
            timeout: 超时时间（毫秒）
        """
        logger.info(f"断言元素隐藏: {selector}")
        try:
            locator = self._get_locator(selector)
            expect(locator).to_be_hidden(timeout=timeout)
        except AssertionError as e:
            logger.error(f"元素隐藏断言失败: {selector}")
            raise

    def assert_element_enabled(self, selector: str) -> None:
        """断言元素启用"""
        logger.info(f"断言元素启用: {selector}")
        try:
            locator = self._get_locator(selector)
            expect(locator).to_be_enabled()
        except AssertionError as e:
            logger.error(f"元素启用断言失败: {selector}")
            raise

    def assert_element_disabled(self, selector: str) -> None:
        """断言元素禁用"""
        logger.info(f"断言元素禁用: {selector}")
        try:
            locator = self._get_locator(selector)
            expect(locator).to_be_disabled()
        except AssertionError as e:
            logger.error(f"元素禁用断言失败: {selector}")
            raise

    # ==================== 截图和调试 ====================

    def take_screenshot(self, name: str = None) -> Path:
        """
        截图

        Args:
            name: 截图名称

        Returns:
            截图文件路径
        """
        if name is None:
            name = f"screenshot_{int(time.time())}"

        # 截图存储在当日时间里
        today_date = datetime.now().strftime("%Y-%m-%d")
        daily_dir = ScreenshotConfig.SCREENSHOT_DIR / today_date
        # 有则跳过，无则创建
        daily_dir.mkdir(parents=True, exist_ok=True)

        screenshot_path = daily_dir / f"{name}.png"
        self.page.screenshot(path=screenshot_path)
        logger.info(f"截图已保存: {screenshot_path}")
        return screenshot_path

    def get_page_source(self) -> str:
        """获取页面源码"""
        return self.page.content()

    def execute_script(self, script: str) -> Any:
        """
        执行 JavaScript 脚本

        Args:
            script: JavaScript 代码

        Returns:
            脚本执行结果
        """
        logger.debug(f"执行脚本: {script}")
        return self.page.evaluate(script)

    # ==================== 辅助方法 ====================

    def _get_locator(self, selector: Any):
        """
        获取 Locator 对象

        Args:
            selector: CSS 选择器或已有的 Locator 对象

        Returns:
            Locator 对象
        """
        if isinstance(selector, str):
            return self.page.locator(selector)
        return selector

    def is_element_visible(self, selector: str) -> bool:
        """
        检查元素是否可见

        Args:
            selector: CSS 选择器或 Locator

        Returns:
            是否可见
        """
        try:
            locator = self._get_locator(selector)
            return locator.is_visible()
        except Exception:
            return False

    def is_element_enabled(self, selector: str) -> bool:
        """
        检查元素是否启用

        Args:
            selector: CSS 选择器或 Locator

        Returns:
            是否启用
        """
        try:
            locator = self._get_locator(selector)
            return locator.is_enabled()
        except Exception:
            return False

    def is_element_checked(self, selector: str) -> bool:
        """
        检查复选框是否选中

        Args:
            selector: CSS 选择器或 Locator

        Returns:
            是否选中
        """
        try:
            locator = self._get_locator(selector)
            return locator.is_checked()
        except Exception:
            return False

    def get_element_count(self, selector: str) -> int:
        """
        获取匹配元素个数

        Args:
            selector: CSS 选择器或 Locator

        Returns:
            元素个数
        """
        locator = self._get_locator(selector)
        return locator.count()

    def scroll_into_view(self, selector: str) -> None:
        """
        将元素滚动到可视区域

        Args:
            selector: CSS 选择器或 Locator
        """
        logger.info(f"滚动元素到可视区: {selector}")
        locator = self._get_locator(selector)
        locator.scroll_into_view_if_needed()

    def hover(self, selector: str) -> None:
        """
        鼠标悬停

        Args:
            selector: CSS 选择器或 Locator
        """
        logger.info(f"鼠标悬停: {selector}")
        locator = self._get_locator(selector)
        locator.hover()

    def double_click(self, selector: str) -> None:
        """
        双击

        Args:
            selector: CSS 选择器或 Locator
        """
        logger.info(f"双击: {selector}")
        locator = self._get_locator(selector)
        locator.dblclick()

    def right_click(self, selector: str) -> None:
        """
        右击

        Args:
            selector: CSS 选择器或 Locator
        """
        logger.info(f"右击: {selector}")
        locator = self._get_locator(selector)
        locator.click(button="right")
import json
import os
from pathlib import Path
from dotenv import load_dotenv  # 导入 load_dotenv方法



# 项目根路径
BASE_DIR = Path(__file__).parent.parent

# 获取本地 .env 文件里的 环境变量, 这是使用的是 绝对路径位置，防止找不到文件路径
env = BASE_DIR / ".env"
load_dotenv(dotenv_path=env)

class BrowserConfig:
    """浏览器配置"""
    HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
    BROWSER_TYPE = os.getenv("BROWSER", "chromium")
    SLOW_MO = int(os.getenv("SLOW_MO", "100"))
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))

    # 添加 args 列表参数化：
    _args_str = os.getenv("ARGS", '["--start-maximized"]')  # 先获取字符串
    try:
        Args = json.loads(_args_str)  # 尝试解析为列表
    except json.JSONDecodeError:
        # 如果解析失败（例如，环境变量不是有效的 JSON 格式），可以设置一个默认值或报错
        print(f"Warning: Could not parse ARGS environment variable '{_args_str}'. Using empty list.")


    @classmethod    # 类方法-作用：无需实例化类，就可以调用 display方法，即 BrowserConfig.display()
    def display(cls):
        """显示当前浏览器配置"""
        print("\n" + "=" * 50)
        print("浏览器配置:")
        print(f"  类型: {cls.BROWSER_TYPE}")
        print(f"  无头模式: {cls.HEADLESS}")
        print(f"  最大化窗口: {cls.Args}")
        print(f"  最大化窗口: {type(cls.Args)}")
        print(f"  慢动作延迟: {cls.SLOW_MO}ms")
        print(f"  超时时间: {cls.TIMEOUT}ms")
        print("=" * 50 + "\n")
if __name__ == '__main__':
    BrowserConfig.display()




class ScreenshotConfig:
    """截图配置"""
    SCREENSHOT_DIR = BASE_DIR / "screenshots"
    TAKE_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "True").lower() == "true"  # 是否开始截图操作，默认开启

    @classmethod
    def ensure_screenshot_dir(cls):
        """确保截图目录存在"""
        cls.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def display(cls):
        """显示截图配置"""
        print("\n" + "=" * 50)
        print("截图配置:")
        print(f"  截图目录: {cls.SCREENSHOT_DIR}")
        print(f"  失败时截图: {cls.TAKE_ON_FAILURE}")
        print("=" * 50 + "\n")

class LogConfig:
    """日志配置"""
    LOG_DIR = BASE_DIR / "logs"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def ensure_log_dir(cls):
        """确保日志目录存在"""
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def display(cls):
        """显示日志配置"""
        print("\n" + "=" * 50)
        print("日志配置:")
        print(f"  日志目录: {cls.LOG_DIR}")
        print(f"  日志级别: {cls.LOG_LEVEL}")
        print("=" * 50 + "\n")

class ServerConfig:
    """测试服务器配置"""
    BASE_URL = os.getenv("BASE_URL", "http://dev8.kuotian.cc/login")
    LOGIN_URL = f"{BASE_URL}/login"

    @classmethod
    def display(cls):
        """显示当前服务器配置"""
        print("\n" + "=" * 50)
        print("服务器配置:")
        print(f"  基础 URL: {cls.BASE_URL}")
        print(f"  登录 URL: {cls.LOGIN_URL}")
        print("=" * 50 + "\n")
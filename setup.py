"""初始化目录"""

import os
import shutil
from pathlib import Path


def init_project():
    """初始化项目结构"""
    base_dir = Path(__file__).parent

    print("🚀 初始化自动化测试项目...\n")

    # 1. 创建必要的目录
    directories = [
        "logs",     # 存放日志文件
        "screenshots",      # 存放每日操作失败的截图
        "config",   # 存放统一的配置文件
        "pages",    # 页面层
        "tests",    # 测试用例
        "utils",    # 自定义类
        "data"      # 存放元素层与测试数据
    ]

    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(exist_ok=True)
        print(f"✅ 创建目录: {directory}/")

init_project()
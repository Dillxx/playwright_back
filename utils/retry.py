"""
重试装饰器
"""
import time
import functools
from utils.logger import get_logger

logger = get_logger(__name__)


def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 1.0):
    """
    重试装饰器

    Args:
        max_attempts: 最大尝试次数
        delay: 初始延迟时间（秒）
        backoff: 延迟倍增因子
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay

            for attempt in range(1, max_attempts + 1):
                try:
                    logger.info(f"执行 {func.__name__}，尝试次数: {attempt}/{max_attempts}")
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        logger.error(f"{func.__name__} 已重试 {max_attempts} 次，最终失败: {e}")
                        raise

                    logger.warning(
                        f"{func.__name__} 失败，{current_delay}秒后重试. "
                        f"错误: {e}"
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator
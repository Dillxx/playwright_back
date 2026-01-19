"""存储数据层"""

from dataclasses import dataclass

@dataclass
class LoginData:
    """登录数据"""
    username : str
    password : str


# 实例化传值
valid_login = LoginData(
    username='18888888888',
    password='Hqq123456'
)


"""
核心功能模块
提供框架的核心功能和基础类
"""

from .driver_manager import DriverManager
from .page_base import PageBase
from .element_handler import ElementHandler
from .wait_handler import WaitHandler

__all__ = [
    'DriverManager',
    'PageBase', 
    'ElementHandler',
    'WaitHandler'
]

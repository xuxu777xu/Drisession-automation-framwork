"""
页面基类
提供页面对象模式(POM)的基础实现
"""

from typing import Union, Optional, Any, Dict, List
from abc import ABC, abstractmethod
from DrissionPage import ChromiumPage, SessionPage, WebPage
from DrissionPage.items import ChromiumElement, SessionElement
from loguru import logger
from config import settings
from .driver_manager import driver_manager
from .element_handler import ElementHandler
from .wait_handler import WaitHandler
import time


class PageBase(ABC):
    """页面基类 - 所有页面对象的基类"""
    
    def __init__(
        self,
        driver: Optional[Union[ChromiumPage, SessionPage, WebPage]] = None,
        driver_name: str = "default",
        url: Optional[str] = None
    ):
        """初始化页面对象
        
        Args:
            driver: 页面驱动实例
            driver_name: 驱动名称
            url: 页面URL
        """
        self.driver_name = driver_name
        self.url = url
        self._driver = driver
        
        # 初始化处理器
        self.element_handler = ElementHandler(self)
        self.wait_handler = WaitHandler(self)
        
        # 页面加载时间记录
        self._load_start_time = None
        self._load_end_time = None
        
        logger.info(f"页面对象初始化: {self.__class__.__name__}")
    
    @property
    def driver(self) -> Union[ChromiumPage, SessionPage, WebPage]:
        """获取驱动实例"""
        if self._driver is None:
            self._driver = driver_manager.get_driver(self.driver_name)
            if self._driver is None:
                raise RuntimeError(f"驱动实例不存在: {self.driver_name}")
        return self._driver
    
    @driver.setter
    def driver(self, value: Union[ChromiumPage, SessionPage, WebPage]) -> None:
        """设置驱动实例"""
        self._driver = value
    
    def open(self, url: Optional[str] = None, **kwargs) -> "PageBase":
        """打开页面
        
        Args:
            url: 页面URL，如果为None则使用实例的url
            **kwargs: 其他参数
            
        Returns:
            页面对象自身
        """
        target_url = url or self.url
        if not target_url:
            raise ValueError("未指定页面URL")
        
        self._load_start_time = time.time()
        
        try:
            self.driver.get(target_url, **kwargs)
            self._load_end_time = time.time()
            
            # 等待页面加载完成
            self.wait_for_page_load()
            
            logger.info(f"页面已打开: {target_url}")
            return self
            
        except Exception as e:
            logger.error(f"打开页面失败 {target_url}: {e}")
            raise
    
    def refresh(self) -> "PageBase":
        """刷新页面"""
        try:
            self.driver.refresh()
            self.wait_for_page_load()
            logger.info("页面已刷新")
            return self
        except Exception as e:
            logger.error(f"刷新页面失败: {e}")
            raise
    
    def back(self) -> "PageBase":
        """后退"""
        try:
            if hasattr(self.driver, 'back'):
                self.driver.back()
                self.wait_for_page_load()
                logger.info("页面已后退")
            else:
                logger.warning("当前驱动不支持后退操作")
            return self
        except Exception as e:
            logger.error(f"页面后退失败: {e}")
            raise
    
    def forward(self) -> "PageBase":
        """前进"""
        try:
            if hasattr(self.driver, 'forward'):
                self.driver.forward()
                self.wait_for_page_load()
                logger.info("页面已前进")
            else:
                logger.warning("当前驱动不支持前进操作")
            return self
        except Exception as e:
            logger.error(f"页面前进失败: {e}")
            raise
    
    def get_title(self) -> str:
        """获取页面标题"""
        try:
            return self.driver.title
        except Exception as e:
            logger.error(f"获取页面标题失败: {e}")
            return ""
    
    def get_current_url(self) -> str:
        """获取当前URL"""
        try:
            return self.driver.url
        except Exception as e:
            logger.error(f"获取当前URL失败: {e}")
            return ""
    
    def get_page_source(self) -> str:
        """获取页面源码"""
        try:
            return self.driver.html
        except Exception as e:
            logger.error(f"获取页面源码失败: {e}")
            return ""
    
    def take_screenshot(
        self,
        filename: Optional[str] = None,
        full_page: bool = True
    ) -> str:
        """截图
        
        Args:
            filename: 文件名，如果为None则自动生成
            full_page: 是否全页截图
            
        Returns:
            截图文件路径
        """
        if filename is None:
            timestamp = int(time.time())
            filename = f"{self.__class__.__name__}_{timestamp}.png"
        
        screenshot_path = settings.screenshots_dir / filename
        
        try:
            if hasattr(self.driver, 'get_screenshot'):
                self.driver.get_screenshot(
                    path=str(settings.screenshots_dir),
                    name=filename,
                    full_page=full_page
                )
            else:
                logger.warning("当前驱动不支持截图功能")
                return ""
            
            logger.info(f"截图已保存: {screenshot_path}")
            return str(screenshot_path)
            
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return ""
    
    def execute_script(self, script: str, *args) -> Any:
        """执行JavaScript脚本
        
        Args:
            script: JavaScript代码
            *args: 脚本参数
            
        Returns:
            脚本执行结果
        """
        try:
            if hasattr(self.driver, 'run_js'):
                return self.driver.run_js(script, *args)
            else:
                logger.warning("当前驱动不支持JavaScript执行")
                return None
        except Exception as e:
            logger.error(f"执行JavaScript失败: {e}")
            return None
    
    def switch_to_frame(self, frame_locator: str) -> "PageBase":
        """切换到iframe
        
        Args:
            frame_locator: iframe定位器
            
        Returns:
            页面对象自身
        """
        try:
            if hasattr(self.driver, 'get_frame'):
                frame = self.driver.get_frame(frame_locator)
                if frame:
                    # 更新驱动为frame对象
                    self._driver = frame
                    logger.info(f"已切换到iframe: {frame_locator}")
                else:
                    logger.error(f"未找到iframe: {frame_locator}")
            else:
                logger.warning("当前驱动不支持iframe操作")
            return self
        except Exception as e:
            logger.error(f"切换iframe失败: {e}")
            raise
    
    def switch_to_default_content(self) -> "PageBase":
        """切换回主页面"""
        try:
            # 重新获取主页面驱动
            self._driver = driver_manager.get_driver(self.driver_name)
            logger.info("已切换回主页面")
            return self
        except Exception as e:
            logger.error(f"切换回主页面失败: {e}")
            raise
    
    def wait_for_page_load(self, timeout: Optional[int] = None) -> bool:
        """等待页面加载完成
        
        Args:
            timeout: 超时时间
            
        Returns:
            是否加载成功
        """
        timeout = timeout or settings.page_load_timeout
        
        try:
            if hasattr(self.driver, 'wait'):
                self.driver.wait.load_start(timeout=timeout)
                return True
            else:
                # 简单等待
                time.sleep(2)
                return True
        except Exception as e:
            logger.error(f"等待页面加载失败: {e}")
            return False
    
    def get_load_time(self) -> Optional[float]:
        """获取页面加载时间
        
        Returns:
            加载时间（秒）
        """
        if self._load_start_time and self._load_end_time:
            return self._load_end_time - self._load_start_time
        return None
    
    @abstractmethod
    def is_loaded(self) -> bool:
        """检查页面是否加载完成
        
        子类必须实现此方法来定义页面加载完成的标准
        
        Returns:
            是否加载完成
        """
        pass
    
    @abstractmethod
    def get_page_elements(self) -> Dict[str, str]:
        """获取页面元素定位器
        
        子类必须实现此方法来定义页面元素
        
        Returns:
            元素名称和定位器的字典
        """
        pass
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.__class__.__name__}(url={self.url})"
    
    def __repr__(self) -> str:
        """详细字符串表示"""
        return (
            f"{self.__class__.__name__}("
            f"url={self.url}, "
            f"driver_name={self.driver_name}, "
            f"loaded={self.is_loaded()})"
        )

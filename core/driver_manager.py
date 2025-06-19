"""
驱动管理器
基于DrissionPage 4.0+ API设计，支持多种页面对象管理
"""

from typing import Dict, Optional, Union, Any
from DrissionPage import ChromiumPage, SessionPage, WebPage
from DrissionPage import ChromiumOptions, SessionOptions
from loguru import logger
from config import BrowserConfig, settings
import threading
from contextlib import contextmanager


class DriverManager:
    """驱动管理器 - 管理所有页面对象实例"""
    
    def __init__(self):
        self._drivers: Dict[str, Union[ChromiumPage, SessionPage, WebPage]] = {}
        self._lock = threading.Lock()
        self._default_browser_config = BrowserConfig()
    
    def create_chromium_page(
        self,
        name: str = "default",
        config: Optional[BrowserConfig] = None,
        **kwargs
    ) -> ChromiumPage:
        """创建ChromiumPage实例
        
        Args:
            name: 实例名称
            config: 浏览器配置
            **kwargs: 其他参数
            
        Returns:
            ChromiumPage实例
        """
        with self._lock:
            if name in self._drivers:
                logger.warning(f"驱动实例已存在: {name}, 将覆盖现有实例")
                self.close_driver(name)
            
            # 使用配置或默认配置
            browser_config = config or self._default_browser_config
            chromium_options = browser_config.get_chromium_options()
            
            try:
                # 创建ChromiumPage实例
                page = ChromiumPage(
                    addr_or_opts=chromium_options,
                    timeout=settings.element_timeout,
                    **kwargs
                )
                
                self._drivers[name] = page
                logger.info(f"ChromiumPage实例已创建: {name}")
                return page
                
            except Exception as e:
                logger.error(f"创建ChromiumPage失败: {e}")
                raise
    
    def create_session_page(
        self,
        name: str = "default",
        config: Optional[BrowserConfig] = None,
        **kwargs
    ) -> SessionPage:
        """创建SessionPage实例
        
        Args:
            name: 实例名称
            config: 配置
            **kwargs: 其他参数
            
        Returns:
            SessionPage实例
        """
        with self._lock:
            if name in self._drivers:
                logger.warning(f"驱动实例已存在: {name}, 将覆盖现有实例")
                self.close_driver(name)
            
            # 使用配置或默认配置
            browser_config = config or self._default_browser_config
            session_options = browser_config.get_session_options()
            
            try:
                # 创建SessionPage实例
                page = SessionPage(
                    session_or_options=session_options,
                    timeout=settings.element_timeout,
                    **kwargs
                )
                
                self._drivers[name] = page
                logger.info(f"SessionPage实例已创建: {name}")
                return page
                
            except Exception as e:
                logger.error(f"创建SessionPage失败: {e}")
                raise
    
    def create_web_page(
        self,
        name: str = "default",
        mode: str = "d",
        config: Optional[BrowserConfig] = None,
        **kwargs
    ) -> WebPage:
        """创建WebPage实例
        
        Args:
            name: 实例名称
            mode: 模式 ('d' 浏览器模式, 's' 请求模式)
            config: 配置
            **kwargs: 其他参数
            
        Returns:
            WebPage实例
        """
        with self._lock:
            if name in self._drivers:
                logger.warning(f"驱动实例已存在: {name}, 将覆盖现有实例")
                self.close_driver(name)
            
            # 使用配置或默认配置
            browser_config = config or self._default_browser_config
            
            try:
                # 创建WebPage实例
                if mode == "d":
                    # 浏览器模式
                    page = WebPage(
                        mode=mode,
                        chromium_options=browser_config.get_chromium_options(),
                        session_or_options=browser_config.get_session_options(),
                        timeout=settings.element_timeout,
                        **kwargs
                    )
                else:
                    # 请求模式
                    page = WebPage(
                        mode=mode,
                        session_or_options=browser_config.get_session_options(),
                        timeout=settings.element_timeout,
                        **kwargs
                    )
                
                self._drivers[name] = page
                logger.info(f"WebPage实例已创建: {name}, 模式: {mode}")
                return page
                
            except Exception as e:
                logger.error(f"创建WebPage失败: {e}")
                raise
    
    def get_driver(self, name: str = "default") -> Optional[Union[ChromiumPage, SessionPage, WebPage]]:
        """获取驱动实例
        
        Args:
            name: 实例名称
            
        Returns:
            驱动实例或None
        """
        return self._drivers.get(name)
    
    def close_driver(self, name: str) -> bool:
        """关闭指定驱动实例
        
        Args:
            name: 实例名称
            
        Returns:
            是否成功关闭
        """
        with self._lock:
            if name not in self._drivers:
                logger.warning(f"驱动实例不存在: {name}")
                return False
            
            try:
                driver = self._drivers[name]
                
                # 根据类型执行相应的关闭操作
                if hasattr(driver, 'quit'):
                    driver.quit()
                elif hasattr(driver, 'close'):
                    driver.close()
                
                del self._drivers[name]
                logger.info(f"驱动实例已关闭: {name}")
                return True
                
            except Exception as e:
                logger.error(f"关闭驱动实例失败 {name}: {e}")
                return False
    
    def close_all_drivers(self) -> None:
        """关闭所有驱动实例"""
        with self._lock:
            driver_names = list(self._drivers.keys())
            for name in driver_names:
                self.close_driver(name)
            
            logger.info("所有驱动实例已关闭")
    
    def list_drivers(self) -> Dict[str, str]:
        """列出所有驱动实例
        
        Returns:
            驱动实例名称和类型的字典
        """
        return {
            name: type(driver).__name__
            for name, driver in self._drivers.items()
        }
    
    def get_driver_info(self, name: str) -> Optional[Dict[str, Any]]:
        """获取驱动实例信息
        
        Args:
            name: 实例名称
            
        Returns:
            驱动信息字典或None
        """
        driver = self.get_driver(name)
        if not driver:
            return None
        
        info = {
            "name": name,
            "type": type(driver).__name__,
            "created_at": getattr(driver, '_created_at', None)
        }
        
        # 添加特定类型的信息
        if isinstance(driver, (ChromiumPage, WebPage)):
            try:
                info.update({
                    "url": driver.url,
                    "title": driver.title,
                    "address": getattr(driver, 'address', None)
                })
            except:
                pass
        
        return info
    
    @contextmanager
    def get_temp_driver(
        self,
        driver_type: str = "chromium",
        config: Optional[BrowserConfig] = None,
        **kwargs
    ):
        """临时驱动上下文管理器
        
        Args:
            driver_type: 驱动类型 ('chromium', 'session', 'web')
            config: 配置
            **kwargs: 其他参数
            
        Yields:
            临时驱动实例
        """
        temp_name = f"temp_{id(threading.current_thread())}"
        
        try:
            if driver_type == "chromium":
                driver = self.create_chromium_page(temp_name, config, **kwargs)
            elif driver_type == "session":
                driver = self.create_session_page(temp_name, config, **kwargs)
            elif driver_type == "web":
                driver = self.create_web_page(temp_name, config=config, **kwargs)
            else:
                raise ValueError(f"不支持的驱动类型: {driver_type}")
            
            yield driver
            
        finally:
            self.close_driver(temp_name)
    
    def set_default_config(self, config: BrowserConfig) -> None:
        """设置默认浏览器配置
        
        Args:
            config: 浏览器配置
        """
        self._default_browser_config = config
        logger.info("默认浏览器配置已更新")
    
    def __del__(self):
        """析构函数 - 确保所有驱动都被关闭"""
        try:
            self.close_all_drivers()
        except:
            pass


# 全局驱动管理器实例
driver_manager = DriverManager()

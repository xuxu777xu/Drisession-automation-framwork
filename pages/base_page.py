"""
基础页面类
所有具体页面类的基类
"""

from typing import Dict, Optional, Union
from core.page_base import PageBase
from DrissionPage import ChromiumPage, SessionPage, WebPage
from loguru import logger


class BasePage(PageBase):
    """基础页面类 - 提供通用页面功能"""
    
    def __init__(
        self,
        driver: Optional[Union[ChromiumPage, SessionPage, WebPage]] = None,
        driver_name: str = "default",
        url: Optional[str] = None
    ):
        """初始化基础页面
        
        Args:
            driver: 页面驱动实例
            driver_name: 驱动名称
            url: 页面URL
        """
        super().__init__(driver, driver_name, url)
    
    def is_loaded(self) -> bool:
        """检查页面是否加载完成
        
        基础实现：检查页面标题是否存在
        
        Returns:
            是否加载完成
        """
        try:
            title = self.get_title()
            return bool(title and title.strip())
        except Exception as e:
            logger.error(f"检查页面加载状态失败: {e}")
            return False
    
    def get_page_elements(self) -> Dict[str, str]:
        """获取页面元素定位器
        
        基础实现：返回空字典，子类应该重写此方法
        
        Returns:
            元素名称和定位器的字典
        """
        return {}
    
    def wait_for_page_ready(self, timeout: Optional[int] = None) -> bool:
        """等待页面准备就绪
        
        Args:
            timeout: 超时时间
            
        Returns:
            是否准备就绪
        """
        # 等待页面加载
        if not self.wait_for_page_load(timeout):
            return False
        
        # 等待页面特定条件（子类可重写）
        return self.is_loaded()
    
    def scroll_to_top(self) -> "BasePage":
        """滚动到页面顶部"""
        try:
            self.execute_script("window.scrollTo(0, 0);")
            logger.info("已滚动到页面顶部")
        except Exception as e:
            logger.error(f"滚动到页面顶部失败: {e}")
        return self
    
    def scroll_to_bottom(self) -> "BasePage":
        """滚动到页面底部"""
        try:
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            logger.info("已滚动到页面底部")
        except Exception as e:
            logger.error(f"滚动到页面底部失败: {e}")
        return self
    
    def scroll_by_pixels(self, x: int = 0, y: int = 0) -> "BasePage":
        """按像素滚动
        
        Args:
            x: 水平滚动像素
            y: 垂直滚动像素
        """
        try:
            self.execute_script(f"window.scrollBy({x}, {y});")
            logger.info(f"已滚动 ({x}, {y}) 像素")
        except Exception as e:
            logger.error(f"滚动失败: {e}")
        return self
    
    def get_page_info(self) -> Dict[str, str]:
        """获取页面基本信息
        
        Returns:
            页面信息字典
        """
        return {
            "title": self.get_title(),
            "url": self.get_current_url(),
            "page_class": self.__class__.__name__,
            "driver_type": type(self.driver).__name__,
            "loaded": str(self.is_loaded())
        }
    
    def close_current_tab(self) -> "BasePage":
        """关闭当前标签页"""
        try:
            if hasattr(self.driver, 'close'):
                self.driver.close()
                logger.info("当前标签页已关闭")
            else:
                logger.warning("当前驱动不支持关闭标签页")
        except Exception as e:
            logger.error(f"关闭标签页失败: {e}")
        return self
    
    def switch_to_new_tab(self) -> "BasePage":
        """切换到新标签页"""
        try:
            if hasattr(self.driver, 'get_tab'):
                # 等待新标签页出现
                self.wait_handler.wait_for_new_tab()
                
                # 获取最新的标签页
                if hasattr(self.driver, 'tabs'):
                    new_tab = self.driver.get_tab(self.driver.tabs[-1])
                    if new_tab:
                        self._driver = new_tab
                        logger.info("已切换到新标签页")
                    else:
                        logger.error("获取新标签页失败")
                else:
                    logger.warning("当前驱动不支持多标签页操作")
            else:
                logger.warning("当前驱动不支持标签页操作")
        except Exception as e:
            logger.error(f"切换到新标签页失败: {e}")
        return self
    
    def accept_alert(self) -> bool:
        """接受弹窗
        
        Returns:
            是否成功
        """
        try:
            if hasattr(self.driver, 'handle_alert'):
                self.driver.handle_alert(accept=True)
                logger.info("已接受弹窗")
                return True
            else:
                logger.warning("当前驱动不支持弹窗处理")
                return False
        except Exception as e:
            logger.error(f"接受弹窗失败: {e}")
            return False
    
    def dismiss_alert(self) -> bool:
        """取消弹窗
        
        Returns:
            是否成功
        """
        try:
            if hasattr(self.driver, 'handle_alert'):
                self.driver.handle_alert(accept=False)
                logger.info("已取消弹窗")
                return True
            else:
                logger.warning("当前驱动不支持弹窗处理")
                return False
        except Exception as e:
            logger.error(f"取消弹窗失败: {e}")
            return False
    
    def get_alert_text(self) -> str:
        """获取弹窗文本
        
        Returns:
            弹窗文本
        """
        try:
            if hasattr(self.driver, 'alert'):
                alert = self.driver.alert
                if alert:
                    text = alert.text
                    logger.info(f"获取弹窗文本: {text}")
                    return text
            logger.warning("当前驱动不支持弹窗操作或无弹窗")
            return ""
        except Exception as e:
            logger.error(f"获取弹窗文本失败: {e}")
            return ""
    
    def clear_cookies(self) -> "BasePage":
        """清除cookies"""
        try:
            if hasattr(self.driver, 'clear_cookies'):
                self.driver.clear_cookies()
                logger.info("Cookies已清除")
            else:
                logger.warning("当前驱动不支持清除cookies")
        except Exception as e:
            logger.error(f"清除cookies失败: {e}")
        return self
    
    def add_cookie(self, name: str, value: str, **kwargs) -> "BasePage":
        """添加cookie
        
        Args:
            name: cookie名称
            value: cookie值
            **kwargs: 其他cookie属性
        """
        try:
            if hasattr(self.driver, 'set_cookies'):
                cookie_str = f"{name}={value}"
                for key, val in kwargs.items():
                    cookie_str += f"; {key}={val}"
                self.driver.set_cookies(cookie_str)
                logger.info(f"已添加cookie: {name}={value}")
            else:
                logger.warning("当前驱动不支持设置cookies")
        except Exception as e:
            logger.error(f"添加cookie失败: {e}")
        return self

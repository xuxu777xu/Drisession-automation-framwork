"""
等待处理器
基于DrissionPage 4.0+ 等待机制设计
"""

from typing import Callable, Any, Optional, Union
from loguru import logger
import time
from config import settings


class WaitHandler:
    """等待处理器 - 提供各种等待功能"""
    
    def __init__(self, page_obj):
        """初始化等待处理器
        
        Args:
            page_obj: 页面对象
        """
        self.page = page_obj
    
    def wait_for_element_displayed(
        self,
        locator: str,
        timeout: Optional[int] = None
    ) -> bool:
        """等待元素显示
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            
        Returns:
            是否等待成功
        """
        timeout = timeout or settings.element_timeout
        
        try:
            if hasattr(self.page.driver, 'wait'):
                self.page.driver.wait.ele_displayed(locator, timeout=timeout)
                logger.debug(f"元素显示等待成功: {locator}")
                return True
            else:
                # 手动等待
                return self._manual_wait_for_condition(
                    lambda: self.page.element_handler.is_displayed(locator, timeout=1),
                    timeout,
                    f"元素显示: {locator}"
                )
        except Exception as e:
            logger.error(f"等待元素显示失败 {locator}: {e}")
            return False
    
    def wait_for_element_loaded(
        self,
        locator: str,
        timeout: Optional[int] = None
    ) -> bool:
        """等待元素加载
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            
        Returns:
            是否等待成功
        """
        timeout = timeout or settings.element_timeout
        
        try:
            if hasattr(self.page.driver, 'wait'):
                self.page.driver.wait.ele_loaded(locator, timeout=timeout)
                logger.debug(f"元素加载等待成功: {locator}")
                return True
            else:
                # 手动等待
                return self._manual_wait_for_condition(
                    lambda: self.page.element_handler.find_element(locator, timeout=1) is not None,
                    timeout,
                    f"元素加载: {locator}"
                )
        except Exception as e:
            logger.error(f"等待元素加载失败 {locator}: {e}")
            return False
    
    def wait_for_element_deleted(
        self,
        locator: str,
        timeout: Optional[int] = None
    ) -> bool:
        """等待元素删除
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            
        Returns:
            是否等待成功
        """
        timeout = timeout or settings.element_timeout
        
        try:
            if hasattr(self.page.driver, 'wait'):
                element = self.page.element_handler.find_element(locator, timeout=1)
                if element and hasattr(element, 'wait'):
                    element.wait.deleted(timeout=timeout)
                    logger.debug(f"元素删除等待成功: {locator}")
                    return True
            
            # 手动等待
            return self._manual_wait_for_condition(
                lambda: not self.page.element_handler.is_displayed(locator, timeout=1),
                timeout,
                f"元素删除: {locator}"
            )
        except Exception as e:
            logger.error(f"等待元素删除失败 {locator}: {e}")
            return False
    
    def wait_for_page_load(self, timeout: Optional[int] = None) -> bool:
        """等待页面加载完成
        
        Args:
            timeout: 超时时间
            
        Returns:
            是否等待成功
        """
        timeout = timeout or settings.page_load_timeout
        
        try:
            if hasattr(self.page.driver, 'wait'):
                self.page.driver.wait.load_start(timeout=timeout)
                logger.debug("页面加载等待成功")
                return True
            else:
                # 简单等待
                time.sleep(2)
                return True
        except Exception as e:
            logger.error(f"等待页面加载失败: {e}")
            return False
    
    def wait_for_title_contains(
        self,
        text: str,
        timeout: Optional[int] = None
    ) -> bool:
        """等待页面标题包含指定文本
        
        Args:
            text: 期望的文本
            timeout: 超时时间
            
        Returns:
            是否等待成功
        """
        timeout = timeout or settings.element_timeout
        
        return self._manual_wait_for_condition(
            lambda: text in self.page.get_title(),
            timeout,
            f"标题包含: {text}"
        )
    
    def wait_for_url_contains(
        self,
        text: str,
        timeout: Optional[int] = None
    ) -> bool:
        """等待URL包含指定文本
        
        Args:
            text: 期望的文本
            timeout: 超时时间
            
        Returns:
            是否等待成功
        """
        timeout = timeout or settings.element_timeout
        
        return self._manual_wait_for_condition(
            lambda: text in self.page.get_current_url(),
            timeout,
            f"URL包含: {text}"
        )
    
    def wait_for_text_present(
        self,
        text: str,
        timeout: Optional[int] = None
    ) -> bool:
        """等待页面包含指定文本
        
        Args:
            text: 期望的文本
            timeout: 超时时间
            
        Returns:
            是否等待成功
        """
        timeout = timeout or settings.element_timeout
        
        return self._manual_wait_for_condition(
            lambda: text in self.page.get_page_source(),
            timeout,
            f"页面包含文本: {text}"
        )
    
    def wait_for_element_text_equals(
        self,
        locator: str,
        expected_text: str,
        timeout: Optional[int] = None
    ) -> bool:
        """等待元素文本等于指定值
        
        Args:
            locator: 元素定位器
            expected_text: 期望的文本
            timeout: 超时时间
            
        Returns:
            是否等待成功
        """
        timeout = timeout or settings.element_timeout
        
        return self._manual_wait_for_condition(
            lambda: self.page.element_handler.get_text(locator, timeout=1) == expected_text,
            timeout,
            f"元素文本等于: {locator} = '{expected_text}'"
        )
    
    def wait_for_element_text_contains(
        self,
        locator: str,
        expected_text: str,
        timeout: Optional[int] = None
    ) -> bool:
        """等待元素文本包含指定值
        
        Args:
            locator: 元素定位器
            expected_text: 期望的文本
            timeout: 超时时间
            
        Returns:
            是否等待成功
        """
        timeout = timeout or settings.element_timeout
        
        return self._manual_wait_for_condition(
            lambda: expected_text in self.page.element_handler.get_text(locator, timeout=1),
            timeout,
            f"元素文本包含: {locator} 包含 '{expected_text}'"
        )
    
    def wait_for_element_attribute_equals(
        self,
        locator: str,
        attribute: str,
        expected_value: str,
        timeout: Optional[int] = None
    ) -> bool:
        """等待元素属性等于指定值
        
        Args:
            locator: 元素定位器
            attribute: 属性名
            expected_value: 期望的属性值
            timeout: 超时时间
            
        Returns:
            是否等待成功
        """
        timeout = timeout or settings.element_timeout
        
        return self._manual_wait_for_condition(
            lambda: self.page.element_handler.get_attribute(locator, attribute, timeout=1) == expected_value,
            timeout,
            f"元素属性等于: {locator}.{attribute} = '{expected_value}'"
        )
    
    def wait_for_condition(
        self,
        condition: Callable[[], bool],
        timeout: Optional[int] = None,
        description: str = "自定义条件"
    ) -> bool:
        """等待自定义条件
        
        Args:
            condition: 条件函数，返回bool
            timeout: 超时时间
            description: 条件描述
            
        Returns:
            是否等待成功
        """
        timeout = timeout or settings.element_timeout
        
        return self._manual_wait_for_condition(condition, timeout, description)
    
    def wait_for_download_complete(
        self,
        timeout: Optional[int] = None
    ) -> bool:
        """等待下载完成
        
        Args:
            timeout: 超时时间
            
        Returns:
            是否等待成功
        """
        timeout = timeout or 60  # 下载默认等待60秒
        
        try:
            if hasattr(self.page.driver, 'wait'):
                self.page.driver.wait.downloads_done(timeout=timeout)
                logger.debug("下载完成等待成功")
                return True
            else:
                logger.warning("当前驱动不支持下载等待")
                return False
        except Exception as e:
            logger.error(f"等待下载完成失败: {e}")
            return False
    
    def wait_for_new_tab(
        self,
        timeout: Optional[int] = None
    ) -> bool:
        """等待新标签页出现
        
        Args:
            timeout: 超时时间
            
        Returns:
            是否等待成功
        """
        timeout = timeout or settings.element_timeout
        
        try:
            if hasattr(self.page.driver, 'wait'):
                self.page.driver.wait.new_tab(timeout=timeout)
                logger.debug("新标签页等待成功")
                return True
            else:
                logger.warning("当前驱动不支持新标签页等待")
                return False
        except Exception as e:
            logger.error(f"等待新标签页失败: {e}")
            return False
    
    def _manual_wait_for_condition(
        self,
        condition: Callable[[], bool],
        timeout: int,
        description: str
    ) -> bool:
        """手动等待条件满足
        
        Args:
            condition: 条件函数
            timeout: 超时时间
            description: 条件描述
            
        Returns:
            是否等待成功
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                if condition():
                    logger.debug(f"等待条件满足: {description}")
                    return True
            except Exception:
                pass
            
            time.sleep(0.5)
        
        logger.warning(f"等待条件超时: {description}")
        return False
    
    def sleep(self, seconds: float) -> None:
        """简单等待
        
        Args:
            seconds: 等待秒数
        """
        time.sleep(seconds)
        logger.debug(f"等待 {seconds} 秒")

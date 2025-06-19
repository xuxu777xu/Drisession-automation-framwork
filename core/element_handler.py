"""
元素处理器
提供统一的元素操作接口，基于DrissionPage 4.0+ API
"""

from typing import Union, List, Optional, Any, Dict
from DrissionPage.items import ChromiumElement, SessionElement, NoneElement
from loguru import logger
import time
from config import settings


class ElementHandler:
    """元素处理器 - 提供统一的元素操作接口"""
    
    def __init__(self, page_obj):
        """初始化元素处理器
        
        Args:
            page_obj: 页面对象
        """
        self.page = page_obj
    
    def find_element(
        self,
        locator: str,
        timeout: Optional[int] = None
    ) -> Union[ChromiumElement, SessionElement, NoneElement]:
        """查找单个元素
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            
        Returns:
            元素对象
        """
        timeout = timeout or settings.element_timeout
        
        try:
            element = self.page.driver.ele(locator, timeout=timeout)
            if element:
                logger.debug(f"找到元素: {locator}")
            else:
                logger.warning(f"未找到元素: {locator}")
            return element
        except Exception as e:
            logger.error(f"查找元素失败 {locator}: {e}")
            return NoneElement()
    
    def find_elements(
        self,
        locator: str,
        timeout: Optional[int] = None
    ) -> List[Union[ChromiumElement, SessionElement]]:
        """查找多个元素
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            
        Returns:
            元素列表
        """
        timeout = timeout or settings.element_timeout
        
        try:
            elements = self.page.driver.eles(locator, timeout=timeout)
            logger.debug(f"找到 {len(elements)} 个元素: {locator}")
            return elements
        except Exception as e:
            logger.error(f"查找元素列表失败 {locator}: {e}")
            return []
    
    def wait_for_element(
        self,
        locator: str,
        timeout: Optional[int] = None,
        condition: str = "displayed"
    ) -> Union[ChromiumElement, SessionElement, None]:
        """等待元素出现
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            condition: 等待条件 ('displayed', 'loaded', 'clickable')
            
        Returns:
            元素对象或None
        """
        timeout = timeout or settings.element_timeout
        
        try:
            if hasattr(self.page.driver, 'wait'):
                if condition == "displayed":
                    self.page.driver.wait.ele_displayed(locator, timeout=timeout)
                elif condition == "loaded":
                    self.page.driver.wait.ele_loaded(locator, timeout=timeout)
                
                # 获取元素
                element = self.find_element(locator, timeout=1)
                if element and not isinstance(element, NoneElement):
                    logger.debug(f"元素等待成功: {locator}")
                    return element
            
            logger.warning(f"元素等待超时: {locator}")
            return None
            
        except Exception as e:
            logger.error(f"等待元素失败 {locator}: {e}")
            return None
    
    def click_element(
        self,
        locator: str,
        timeout: Optional[int] = None,
        wait_after: float = 0.5
    ) -> bool:
        """点击元素
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            wait_after: 点击后等待时间
            
        Returns:
            是否点击成功
        """
        element = self.wait_for_element(locator, timeout, "displayed")
        if not element:
            return False
        
        try:
            element.click()
            if wait_after > 0:
                time.sleep(wait_after)
            logger.info(f"点击元素成功: {locator}")
            return True
        except Exception as e:
            logger.error(f"点击元素失败 {locator}: {e}")
            return False
    
    def input_text(
        self,
        locator: str,
        text: str,
        clear: bool = True,
        timeout: Optional[int] = None
    ) -> bool:
        """输入文本
        
        Args:
            locator: 元素定位器
            text: 输入文本
            clear: 是否先清空
            timeout: 超时时间
            
        Returns:
            是否输入成功
        """
        element = self.wait_for_element(locator, timeout, "displayed")
        if not element:
            return False
        
        try:
            if clear:
                element.clear()
            element.input(text)
            logger.info(f"输入文本成功: {locator} = '{text}'")
            return True
        except Exception as e:
            logger.error(f"输入文本失败 {locator}: {e}")
            return False
    
    def get_text(
        self,
        locator: str,
        timeout: Optional[int] = None
    ) -> str:
        """获取元素文本
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            
        Returns:
            元素文本
        """
        element = self.find_element(locator, timeout)
        if not element or isinstance(element, NoneElement):
            return ""
        
        try:
            text = element.text
            logger.debug(f"获取文本: {locator} = '{text}'")
            return text
        except Exception as e:
            logger.error(f"获取文本失败 {locator}: {e}")
            return ""
    
    def get_attribute(
        self,
        locator: str,
        attribute: str,
        timeout: Optional[int] = None
    ) -> str:
        """获取元素属性
        
        Args:
            locator: 元素定位器
            attribute: 属性名
            timeout: 超时时间
            
        Returns:
            属性值
        """
        element = self.find_element(locator, timeout)
        if not element or isinstance(element, NoneElement):
            return ""
        
        try:
            value = element.attr(attribute)
            logger.debug(f"获取属性: {locator}.{attribute} = '{value}'")
            return value or ""
        except Exception as e:
            logger.error(f"获取属性失败 {locator}.{attribute}: {e}")
            return ""
    
    def set_attribute(
        self,
        locator: str,
        attribute: str,
        value: str,
        timeout: Optional[int] = None
    ) -> bool:
        """设置元素属性
        
        Args:
            locator: 元素定位器
            attribute: 属性名
            value: 属性值
            timeout: 超时时间
            
        Returns:
            是否设置成功
        """
        element = self.find_element(locator, timeout)
        if not element or isinstance(element, NoneElement):
            return False
        
        try:
            if hasattr(element, 'set'):
                element.set.attr(attribute, value)
                logger.info(f"设置属性成功: {locator}.{attribute} = '{value}'")
                return True
            else:
                logger.warning(f"元素不支持设置属性: {locator}")
                return False
        except Exception as e:
            logger.error(f"设置属性失败 {locator}.{attribute}: {e}")
            return False
    
    def is_displayed(
        self,
        locator: str,
        timeout: Optional[int] = None
    ) -> bool:
        """检查元素是否显示
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            
        Returns:
            是否显示
        """
        element = self.find_element(locator, timeout)
        if not element or isinstance(element, NoneElement):
            return False
        
        try:
            # 对于ChromiumElement，检查是否显示
            if hasattr(element, 'states'):
                return element.states.is_displayed
            # 对于SessionElement，如果能找到就认为是显示的
            return True
        except Exception as e:
            logger.error(f"检查元素显示状态失败 {locator}: {e}")
            return False
    
    def is_enabled(
        self,
        locator: str,
        timeout: Optional[int] = None
    ) -> bool:
        """检查元素是否可用
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            
        Returns:
            是否可用
        """
        element = self.find_element(locator, timeout)
        if not element or isinstance(element, NoneElement):
            return False
        
        try:
            if hasattr(element, 'states'):
                return element.states.is_enabled
            # 对于SessionElement，检查disabled属性
            return not element.attr('disabled')
        except Exception as e:
            logger.error(f"检查元素可用状态失败 {locator}: {e}")
            return False
    
    def hover_element(
        self,
        locator: str,
        timeout: Optional[int] = None
    ) -> bool:
        """悬停元素
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            
        Returns:
            是否悬停成功
        """
        element = self.wait_for_element(locator, timeout, "displayed")
        if not element:
            return False
        
        try:
            if hasattr(element, 'hover'):
                element.hover()
                logger.info(f"悬停元素成功: {locator}")
                return True
            else:
                logger.warning(f"元素不支持悬停操作: {locator}")
                return False
        except Exception as e:
            logger.error(f"悬停元素失败 {locator}: {e}")
            return False
    
    def scroll_to_element(
        self,
        locator: str,
        timeout: Optional[int] = None
    ) -> bool:
        """滚动到元素
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            
        Returns:
            是否滚动成功
        """
        element = self.find_element(locator, timeout)
        if not element or isinstance(element, NoneElement):
            return False
        
        try:
            if hasattr(element, 'scroll'):
                element.scroll.to_see()
                logger.info(f"滚动到元素成功: {locator}")
                return True
            else:
                logger.warning(f"元素不支持滚动操作: {locator}")
                return False
        except Exception as e:
            logger.error(f"滚动到元素失败 {locator}: {e}")
            return False
    
    def get_element_screenshot(
        self,
        locator: str,
        filename: Optional[str] = None,
        timeout: Optional[int] = None
    ) -> str:
        """获取元素截图
        
        Args:
            locator: 元素定位器
            filename: 文件名
            timeout: 超时时间
            
        Returns:
            截图文件路径
        """
        element = self.find_element(locator, timeout)
        if not element or isinstance(element, NoneElement):
            return ""
        
        if filename is None:
            timestamp = int(time.time())
            filename = f"element_{timestamp}.png"
        
        try:
            if hasattr(element, 'get_screenshot'):
                screenshot_path = settings.screenshots_dir / filename
                element.get_screenshot(
                    path=str(settings.screenshots_dir),
                    name=filename
                )
                logger.info(f"元素截图已保存: {screenshot_path}")
                return str(screenshot_path)
            else:
                logger.warning(f"元素不支持截图功能: {locator}")
                return ""
        except Exception as e:
            logger.error(f"元素截图失败 {locator}: {e}")
            return ""

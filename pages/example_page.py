"""
示例页面类
展示如何使用页面对象模式
"""

from typing import Dict, Optional, Union
from .base_page import BasePage
from DrissionPage import ChromiumPage, SessionPage, WebPage
from loguru import logger


class ExamplePage(BasePage):
    """示例页面 - 以百度首页为例"""
    
    def __init__(
        self,
        driver: Optional[Union[ChromiumPage, SessionPage, WebPage]] = None,
        driver_name: str = "default"
    ):
        """初始化示例页面"""
        super().__init__(
            driver=driver,
            driver_name=driver_name,
            url="https://www.baidu.com"
        )
    
    def get_page_elements(self) -> Dict[str, str]:
        """获取页面元素定位器"""
        return {
            "search_input": "#kw",
            "search_button": "#su",
            "search_results": "#content_left",
            "result_items": ".result",
            "result_titles": ".result h3",
            "logo": "#lg img",
            "hot_search": "#hotsearch-content-wrapper",
            "settings_link": "#s-usersetting-top",
            "news_link": 'a[href*="news.baidu.com"]',
            "images_link": 'a[href*="image.baidu.com"]',
            "videos_link": 'a[href*="video.baidu.com"]',
            "maps_link": 'a[href*="map.baidu.com"]'
        }
    
    def is_loaded(self) -> bool:
        """检查页面是否加载完成"""
        try:
            # 检查搜索框是否存在
            search_input_exists = self.element_handler.is_displayed(
                self.get_page_elements()["search_input"],
                timeout=5
            )
            
            # 检查页面标题
            title_correct = "百度" in self.get_title()
            
            return search_input_exists and title_correct
            
        except Exception as e:
            logger.error(f"检查页面加载状态失败: {e}")
            return False
    
    def search(self, keyword: str) -> bool:
        """执行搜索
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            是否搜索成功
        """
        elements = self.get_page_elements()
        
        try:
            # 输入搜索关键词
            if not self.element_handler.input_text(
                elements["search_input"],
                keyword,
                clear=True
            ):
                logger.error("输入搜索关键词失败")
                return False
            
            # 点击搜索按钮
            if not self.element_handler.click_element(elements["search_button"]):
                logger.error("点击搜索按钮失败")
                return False
            
            # 等待搜索结果加载
            if not self.wait_handler.wait_for_element_displayed(
                elements["search_results"],
                timeout=10
            ):
                logger.error("等待搜索结果失败")
                return False
            
            logger.info(f"搜索成功: {keyword}")
            return True
            
        except Exception as e:
            logger.error(f"搜索失败: {e}")
            return False
    
    def get_search_results(self) -> list:
        """获取搜索结果
        
        Returns:
            搜索结果列表
        """
        elements = self.get_page_elements()
        results = []
        
        try:
            # 获取所有结果项
            result_elements = self.element_handler.find_elements(
                elements["result_items"]
            )
            
            for element in result_elements:
                try:
                    # 获取标题
                    title_element = element.ele("h3", timeout=1)
                    title = title_element.text if title_element else ""
                    
                    # 获取链接
                    link_element = element.ele("h3 a", timeout=1)
                    link = link_element.attr("href") if link_element else ""
                    
                    # 获取描述
                    desc_element = element.ele(".c-abstract", timeout=1)
                    description = desc_element.text if desc_element else ""
                    
                    if title:  # 只添加有标题的结果
                        results.append({
                            "title": title,
                            "link": link,
                            "description": description
                        })
                        
                except Exception as e:
                    logger.debug(f"解析搜索结果项失败: {e}")
                    continue
            
            logger.info(f"获取到 {len(results)} 个搜索结果")
            return results
            
        except Exception as e:
            logger.error(f"获取搜索结果失败: {e}")
            return []
    
    def click_search_result(self, index: int = 0) -> bool:
        """点击搜索结果
        
        Args:
            index: 结果索引（从0开始）
            
        Returns:
            是否点击成功
        """
        elements = self.get_page_elements()
        
        try:
            result_elements = self.element_handler.find_elements(
                elements["result_titles"]
            )
            
            if index >= len(result_elements):
                logger.error(f"搜索结果索引超出范围: {index}")
                return False
            
            # 点击指定索引的结果
            target_element = result_elements[index]
            link_element = target_element.ele("a", timeout=1)
            
            if link_element:
                link_element.click()
                logger.info(f"点击搜索结果成功: 索引 {index}")
                return True
            else:
                logger.error(f"未找到搜索结果链接: 索引 {index}")
                return False
                
        except Exception as e:
            logger.error(f"点击搜索结果失败: {e}")
            return False
    
    def get_hot_searches(self) -> list:
        """获取热搜列表
        
        Returns:
            热搜关键词列表
        """
        elements = self.get_page_elements()
        hot_searches = []
        
        try:
            # 检查热搜区域是否存在
            if not self.element_handler.is_displayed(elements["hot_search"]):
                logger.info("热搜区域不可见")
                return []
            
            # 获取热搜项
            hot_search_items = self.element_handler.find_elements(
                f'{elements["hot_search"]} a'
            )
            
            for item in hot_search_items:
                try:
                    text = item.text.strip()
                    if text:
                        hot_searches.append(text)
                except Exception:
                    continue
            
            logger.info(f"获取到 {len(hot_searches)} 个热搜关键词")
            return hot_searches
            
        except Exception as e:
            logger.error(f"获取热搜失败: {e}")
            return []
    
    def navigate_to_news(self) -> bool:
        """导航到新闻页面
        
        Returns:
            是否导航成功
        """
        elements = self.get_page_elements()
        
        try:
            if self.element_handler.click_element(elements["news_link"]):
                # 等待页面跳转
                self.wait_handler.wait_for_url_contains("news.baidu.com")
                logger.info("导航到新闻页面成功")
                return True
            else:
                logger.error("点击新闻链接失败")
                return False
                
        except Exception as e:
            logger.error(f"导航到新闻页面失败: {e}")
            return False
    
    def navigate_to_images(self) -> bool:
        """导航到图片页面
        
        Returns:
            是否导航成功
        """
        elements = self.get_page_elements()
        
        try:
            if self.element_handler.click_element(elements["images_link"]):
                # 等待页面跳转
                self.wait_handler.wait_for_url_contains("image.baidu.com")
                logger.info("导航到图片页面成功")
                return True
            else:
                logger.error("点击图片链接失败")
                return False
                
        except Exception as e:
            logger.error(f"导航到图片页面失败: {e}")
            return False
    
    def get_suggestion_keywords(self, keyword: str) -> list:
        """获取搜索建议
        
        Args:
            keyword: 输入的关键词
            
        Returns:
            建议关键词列表
        """
        elements = self.get_page_elements()
        suggestions = []
        
        try:
            # 输入关键词但不搜索
            self.element_handler.input_text(
                elements["search_input"],
                keyword,
                clear=True
            )
            
            # 等待建议出现
            self.wait_handler.sleep(1)
            
            # 获取建议项
            suggestion_elements = self.element_handler.find_elements(
                ".bdsug li"
            )
            
            for element in suggestion_elements:
                try:
                    text = element.text.strip()
                    if text and text != keyword:
                        suggestions.append(text)
                except Exception:
                    continue
            
            logger.info(f"获取到 {len(suggestions)} 个搜索建议")
            return suggestions
            
        except Exception as e:
            logger.error(f"获取搜索建议失败: {e}")
            return []

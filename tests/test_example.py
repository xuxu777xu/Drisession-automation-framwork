"""
示例测试用例
展示如何使用框架进行测试
"""

import pytest
from pages.example_page import ExamplePage
from utils.logger import TestLogger


class TestExamplePage:
    """示例页面测试类"""
    
    @pytest.mark.smoke
    def test_page_load(self, chromium_driver):
        """测试页面加载"""
        test_logger = TestLogger("页面加载测试")
        test_logger.test_start()
        
        try:
            test_logger.step("创建页面对象")
            page = ExamplePage(chromium_driver)
            
            test_logger.step("打开页面")
            page.open()
            
            test_logger.step("验证页面加载")
            assert page.is_loaded(), "页面加载失败"
            
            test_logger.step("验证页面标题")
            title = page.get_title()
            assert "百度" in title, f"页面标题不正确: {title}"
            
            test_logger.test_end("PASS")
            
        except Exception as e:
            test_logger.error(f"测试失败: {e}")
            test_logger.test_end("FAIL")
            raise
    
    @pytest.mark.smoke
    def test_search_functionality(self, chromium_driver):
        """测试搜索功能"""
        test_logger = TestLogger("搜索功能测试")
        test_logger.test_start()
        
        try:
            test_logger.step("创建页面对象")
            page = ExamplePage(chromium_driver)
            
            test_logger.step("打开页面")
            page.open()
            
            test_logger.step("执行搜索")
            search_keyword = "DrissionPage"
            assert page.search(search_keyword), "搜索执行失败"
            
            test_logger.step("获取搜索结果")
            results = page.get_search_results()
            assert len(results) > 0, "未获取到搜索结果"
            
            test_logger.step("验证搜索结果")
            # 验证至少有一个结果包含搜索关键词
            found_keyword = any(
                search_keyword.lower() in result.get('title', '').lower() 
                for result in results
            )
            assert found_keyword, f"搜索结果中未找到关键词: {search_keyword}"
            
            test_logger.success(f"搜索成功，获取到 {len(results)} 个结果")
            test_logger.test_end("PASS")
            
        except Exception as e:
            test_logger.error(f"测试失败: {e}")
            test_logger.test_end("FAIL")
            raise
    
    @pytest.mark.regression
    def test_search_suggestions(self, chromium_driver):
        """测试搜索建议功能"""
        test_logger = TestLogger("搜索建议测试")
        test_logger.test_start()
        
        try:
            test_logger.step("创建页面对象")
            page = ExamplePage(chromium_driver)
            
            test_logger.step("打开页面")
            page.open()
            
            test_logger.step("获取搜索建议")
            suggestions = page.get_suggestion_keywords("Python")
            
            # 搜索建议可能为空，这是正常的
            test_logger.info(f"获取到 {len(suggestions)} 个搜索建议")
            
            if suggestions:
                test_logger.step("验证搜索建议")
                # 验证建议不为空字符串
                valid_suggestions = [s for s in suggestions if s.strip()]
                assert len(valid_suggestions) > 0, "搜索建议为空"
                
                test_logger.success(f"搜索建议验证通过: {valid_suggestions[:3]}")
            
            test_logger.test_end("PASS")
            
        except Exception as e:
            test_logger.error(f"测试失败: {e}")
            test_logger.test_end("FAIL")
            raise
    
    @pytest.mark.regression
    def test_navigation_links(self, chromium_driver):
        """测试导航链接"""
        test_logger = TestLogger("导航链接测试")
        test_logger.test_start()
        
        try:
            test_logger.step("创建页面对象")
            page = ExamplePage(chromium_driver)
            
            test_logger.step("打开页面")
            page.open()
            
            test_logger.step("测试新闻链接")
            # 注意：这个测试可能会跳转到新页面，需要谨慎处理
            current_url = page.get_current_url()
            
            # 检查链接是否存在（不实际点击）
            elements = page.get_page_elements()
            news_link_exists = page.element_handler.is_displayed(
                elements["news_link"], timeout=5
            )
            
            if news_link_exists:
                test_logger.success("新闻链接存在")
            else:
                test_logger.info("新闻链接不可见或不存在")
            
            test_logger.test_end("PASS")
            
        except Exception as e:
            test_logger.error(f"测试失败: {e}")
            test_logger.test_end("FAIL")
            raise
    
    @pytest.mark.slow
    def test_page_performance(self, performance_driver):
        """测试页面性能"""
        from utils.logger import PerformanceLogger
        
        test_logger = TestLogger("页面性能测试")
        perf_logger = PerformanceLogger("页面性能")
        
        test_logger.test_start()
        
        try:
            test_logger.step("创建页面对象")
            page = ExamplePage(performance_driver)
            
            test_logger.step("测试页面加载性能")
            perf_logger.start_timing("页面加载")
            page.open()
            load_time = perf_logger.end_timing("页面加载")
            
            # 验证加载时间在合理范围内（10秒）
            assert load_time < 10, f"页面加载时间过长: {load_time}秒"
            
            test_logger.step("测试搜索性能")
            perf_logger.start_timing("搜索操作")
            page.search("性能测试")
            search_time = perf_logger.end_timing("搜索操作")
            
            # 验证搜索时间在合理范围内（5秒）
            assert search_time < 5, f"搜索时间过长: {search_time}秒"
            
            test_logger.step("记录内存使用")
            perf_logger.log_memory_usage()
            
            # 获取性能摘要
            perf_summary = perf_logger.get_performance_summary()
            test_logger.info(f"性能摘要: {perf_summary}")
            
            test_logger.test_end("PASS")
            
        except Exception as e:
            test_logger.error(f"测试失败: {e}")
            test_logger.test_end("FAIL")
            raise


class TestSessionMode:
    """Session模式测试类"""
    
    @pytest.mark.smoke
    def test_session_page_access(self, session_driver):
        """测试Session模式页面访问"""
        test_logger = TestLogger("Session模式测试")
        test_logger.test_start()
        
        try:
            test_logger.step("创建页面对象")
            page = ExamplePage(session_driver)
            
            test_logger.step("使用Session模式访问页面")
            page.open()
            
            test_logger.step("验证页面内容")
            page_source = page.get_page_source()
            assert "百度" in page_source, "页面内容验证失败"
            
            test_logger.step("验证页面标题")
            title = page.get_title()
            assert title, "页面标题为空"
            
            test_logger.success("Session模式访问成功")
            test_logger.test_end("PASS")
            
        except Exception as e:
            test_logger.error(f"测试失败: {e}")
            test_logger.test_end("FAIL")
            raise


class TestDriverManagement:
    """驱动管理测试类"""
    
    @pytest.mark.regression
    def test_multiple_drivers(self):
        """测试多驱动管理"""
        from core.driver_manager import driver_manager
        from config.browser_config import BrowserPresets
        
        test_logger = TestLogger("多驱动管理测试")
        test_logger.test_start()
        
        try:
            test_logger.step("创建多个驱动实例")
            config = BrowserPresets.headless()
            
            # 创建多个不同类型的驱动
            chromium_driver = driver_manager.create_chromium_page("multi_test_1", config)
            session_driver = driver_manager.create_session_page("multi_test_2", config)
            web_driver = driver_manager.create_web_page("multi_test_3", "s", config)
            
            test_logger.step("验证驱动列表")
            drivers = driver_manager.list_drivers()
            assert "multi_test_1" in drivers, "ChromiumPage驱动未创建"
            assert "multi_test_2" in drivers, "SessionPage驱动未创建"
            assert "multi_test_3" in drivers, "WebPage驱动未创建"
            
            test_logger.step("验证驱动信息")
            for name in ["multi_test_1", "multi_test_2", "multi_test_3"]:
                info = driver_manager.get_driver_info(name)
                assert info is not None, f"驱动信息获取失败: {name}"
                assert info["name"] == name, f"驱动名称不匹配: {name}"
            
            test_logger.step("清理驱动")
            for name in ["multi_test_1", "multi_test_2", "multi_test_3"]:
                assert driver_manager.close_driver(name), f"驱动关闭失败: {name}"
            
            test_logger.success("多驱动管理测试通过")
            test_logger.test_end("PASS")
            
        except Exception as e:
            test_logger.error(f"测试失败: {e}")
            test_logger.test_end("FAIL")
            # 确保清理
            for name in ["multi_test_1", "multi_test_2", "multi_test_3"]:
                driver_manager.close_driver(name)
            raise
    
    @pytest.mark.regression
    def test_temp_driver_context(self):
        """测试临时驱动上下文管理器"""
        from core.driver_manager import driver_manager
        from config.browser_config import BrowserPresets
        
        test_logger = TestLogger("临时驱动测试")
        test_logger.test_start()
        
        try:
            test_logger.step("使用临时驱动上下文")
            config = BrowserPresets.headless()
            
            with driver_manager.get_temp_driver("session", config) as temp_driver:
                test_logger.step("验证临时驱动")
                assert temp_driver is not None, "临时驱动创建失败"
                
                # 使用临时驱动
                page = ExamplePage(temp_driver)
                page.open()
                
                title = page.get_title()
                assert title, "临时驱动页面访问失败"
            
            test_logger.success("临时驱动上下文管理器测试通过")
            test_logger.test_end("PASS")
            
        except Exception as e:
            test_logger.error(f"测试失败: {e}")
            test_logger.test_end("FAIL")
            raise

"""
基础使用示例
展示如何使用DrissionPage自动化框架
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.driver_manager import driver_manager
from config.browser_config import BrowserPresets
from pages.example_page import ExamplePage
from utils.logger import TestLogger, PerformanceLogger
import time


def example_basic_search():
    """基础搜索示例"""
    test_logger = TestLogger("基础搜索测试")
    perf_logger = PerformanceLogger("搜索性能")
    
    try:
        test_logger.test_start()
        
        # 步骤1: 创建浏览器配置
        test_logger.step("创建浏览器配置")
        config = BrowserPresets.default()
        
        # 步骤2: 创建页面驱动
        test_logger.step("创建ChromiumPage驱动")
        perf_logger.start_timing("创建驱动")
        driver = driver_manager.create_chromium_page("search_test", config)
        perf_logger.end_timing("创建驱动")
        
        # 步骤3: 创建页面对象
        test_logger.step("创建页面对象")
        page = ExamplePage(driver)
        
        # 步骤4: 打开页面
        test_logger.step("打开百度首页")
        perf_logger.start_timing("页面加载")
        page.open()
        perf_logger.end_timing("页面加载")
        
        # 验证页面加载
        if not page.is_loaded():
            test_logger.error("页面加载失败")
            return False
        
        test_logger.success("页面加载成功")
        
        # 步骤5: 执行搜索
        test_logger.step("执行搜索")
        search_keyword = "DrissionPage"
        perf_logger.start_timing("搜索操作")
        
        if not page.search(search_keyword):
            test_logger.error("搜索失败")
            return False
        
        perf_logger.end_timing("搜索操作")
        test_logger.success(f"搜索成功: {search_keyword}")
        
        # 步骤6: 获取搜索结果
        test_logger.step("获取搜索结果")
        perf_logger.start_timing("获取结果")
        results = page.get_search_results()
        perf_logger.end_timing("获取结果")
        
        if results:
            test_logger.success(f"获取到 {len(results)} 个搜索结果")
            
            # 显示前3个结果
            for i, result in enumerate(results[:3]):
                test_logger.info(f"结果 {i+1}: {result['title']}")
        else:
            test_logger.warning("未获取到搜索结果")
        
        # 步骤7: 截图
        test_logger.step("保存截图")
        screenshot_path = page.take_screenshot("search_results.png")
        if screenshot_path:
            test_logger.success(f"截图已保存: {screenshot_path}")
        
        test_logger.test_end("PASS")
        return True
        
    except Exception as e:
        test_logger.error(f"测试执行失败: {e}")
        test_logger.test_end("FAIL")
        return False
    
    finally:
        # 清理资源
        driver_manager.close_driver("search_test")
        
        # 输出性能摘要
        perf_summary = perf_logger.get_performance_summary()
        test_logger.info(f"性能摘要: {perf_summary}")


def example_multi_tab_operation():
    """多标签页操作示例"""
    test_logger = TestLogger("多标签页操作测试")
    
    try:
        test_logger.test_start()
        
        # 创建配置
        test_logger.step("创建浏览器配置")
        config = BrowserPresets.default()
        
        # 创建驱动
        test_logger.step("创建WebPage驱动")
        driver = driver_manager.create_web_page("multi_tab_test", "d", config)
        
        # 创建页面对象
        page = ExamplePage(driver)
        
        # 打开首页
        test_logger.step("打开百度首页")
        page.open()
        
        # 搜索并点击结果
        test_logger.step("搜索并点击第一个结果")
        page.search("Python自动化")
        
        # 点击第一个搜索结果（会打开新标签页）
        if page.click_search_result(0):
            test_logger.success("点击搜索结果成功")
            
            # 切换到新标签页
            test_logger.step("切换到新标签页")
            page.switch_to_new_tab()
            
            # 获取新页面信息
            new_page_info = page.get_page_info()
            test_logger.info(f"新页面信息: {new_page_info}")
        
        test_logger.test_end("PASS")
        return True
        
    except Exception as e:
        test_logger.error(f"测试执行失败: {e}")
        test_logger.test_end("FAIL")
        return False
    
    finally:
        driver_manager.close_driver("multi_tab_test")


def example_session_mode():
    """Session模式示例"""
    test_logger = TestLogger("Session模式测试")
    
    try:
        test_logger.test_start()
        
        # 创建Session配置
        test_logger.step("创建Session配置")
        config = BrowserPresets.default()
        
        # 创建SessionPage驱动
        test_logger.step("创建SessionPage驱动")
        driver = driver_manager.create_session_page("session_test", config)
        
        # 创建页面对象
        page = ExamplePage(driver)
        
        # 打开页面（Session模式）
        test_logger.step("使用Session模式访问页面")
        page.open()
        
        # 获取页面源码
        test_logger.step("获取页面源码")
        page_source = page.get_page_source()
        
        if "百度" in page_source:
            test_logger.success("Session模式访问成功")
        else:
            test_logger.error("Session模式访问失败")
            return False
        
        test_logger.test_end("PASS")
        return True
        
    except Exception as e:
        test_logger.error(f"测试执行失败: {e}")
        test_logger.test_end("FAIL")
        return False
    
    finally:
        driver_manager.close_driver("session_test")


def example_performance_mode():
    """性能模式示例"""
    test_logger = TestLogger("性能模式测试")
    perf_logger = PerformanceLogger("性能模式")
    
    try:
        test_logger.test_start()
        
        # 创建性能优化配置
        test_logger.step("创建性能优化配置")
        config = BrowserPresets.performance()
        
        # 创建驱动
        test_logger.step("创建性能优化驱动")
        perf_logger.start_timing("创建驱动")
        driver = driver_manager.create_chromium_page("perf_test", config)
        perf_logger.end_timing("创建驱动")
        
        # 创建页面对象
        page = ExamplePage(driver)
        
        # 测试页面加载性能
        test_logger.step("测试页面加载性能")
        perf_logger.start_timing("页面加载")
        page.open()
        perf_logger.end_timing("页面加载")
        
        # 测试搜索性能
        test_logger.step("测试搜索性能")
        perf_logger.start_timing("搜索操作")
        page.search("性能测试")
        perf_logger.end_timing("搜索操作")
        
        # 记录内存使用
        perf_logger.log_memory_usage()
        
        test_logger.test_end("PASS")
        return True
        
    except Exception as e:
        test_logger.error(f"测试执行失败: {e}")
        test_logger.test_end("FAIL")
        return False
    
    finally:
        driver_manager.close_driver("perf_test")
        
        # 输出性能报告
        perf_summary = perf_logger.get_performance_summary()
        test_logger.info(f"性能报告: {perf_summary}")


def main():
    """主函数 - 运行所有示例"""
    print("🚀 DrissionPage自动化框架示例")
    print("=" * 50)
    
    examples = [
        ("基础搜索示例", example_basic_search),
        ("多标签页操作示例", example_multi_tab_operation),
        ("Session模式示例", example_session_mode),
        ("性能模式示例", example_performance_mode)
    ]
    
    results = []
    
    for name, func in examples:
        print(f"\n📋 运行示例: {name}")
        print("-" * 30)
        
        start_time = time.time()
        success = func()
        duration = time.time() - start_time
        
        results.append({
            "name": name,
            "success": success,
            "duration": duration
        })
        
        status = "✅ 成功" if success else "❌ 失败"
        print(f"结果: {status} (耗时: {duration:.2f}秒)")
    
    # 输出总结
    print("\n" + "=" * 50)
    print("📊 执行总结:")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["success"])
    total_time = sum(r["duration"] for r in results)
    
    print(f"总测试数: {total_tests}")
    print(f"通过数: {passed_tests}")
    print(f"失败数: {total_tests - passed_tests}")
    print(f"总耗时: {total_time:.2f}秒")
    
    # 详细结果
    for result in results:
        status = "✅" if result["success"] else "❌"
        print(f"{status} {result['name']} - {result['duration']:.2f}秒")


if __name__ == "__main__":
    main()

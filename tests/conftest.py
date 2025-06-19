"""
pytest配置文件
定义测试夹具和配置
"""

import pytest
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.driver_manager import driver_manager
from config.browser_config import BrowserPresets
from utils.report_generator import report_generator


@pytest.fixture(scope="session")
def test_session():
    """测试会话夹具"""
    report_generator.start_test_session()
    yield
    report_generator.end_test_session()
    
    # 生成测试报告
    html_report = report_generator.generate_html_report()
    json_report = report_generator.generate_json_report()
    
    print(f"\n📊 测试报告已生成:")
    print(f"HTML报告: {html_report}")
    print(f"JSON报告: {json_report}")


@pytest.fixture
def chromium_driver():
    """ChromiumPage驱动夹具"""
    config = BrowserPresets.default()
    driver = driver_manager.create_chromium_page("test_chromium", config)
    yield driver
    driver_manager.close_driver("test_chromium")


@pytest.fixture
def session_driver():
    """SessionPage驱动夹具"""
    config = BrowserPresets.default()
    driver = driver_manager.create_session_page("test_session", config)
    yield driver
    driver_manager.close_driver("test_session")


@pytest.fixture
def web_driver():
    """WebPage驱动夹具"""
    config = BrowserPresets.default()
    driver = driver_manager.create_web_page("test_web", "d", config)
    yield driver
    driver_manager.close_driver("test_web")


@pytest.fixture
def headless_driver():
    """无头模式驱动夹具"""
    config = BrowserPresets.headless()
    driver = driver_manager.create_chromium_page("test_headless", config)
    yield driver
    driver_manager.close_driver("test_headless")


@pytest.fixture
def performance_driver():
    """性能模式驱动夹具"""
    config = BrowserPresets.performance()
    driver = driver_manager.create_chromium_page("test_performance", config)
    yield driver
    driver_manager.close_driver("test_performance")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试结果钩子"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call":
        # 记录测试结果
        test_result = {
            "name": item.name,
            "description": item.function.__doc__ or "",
            "status": "PASS" if rep.passed else "FAIL" if rep.failed else "SKIP",
            "duration": rep.duration,
            "error": str(rep.longrepr) if rep.failed else None
        }
        
        report_generator.add_test_result(test_result)


def pytest_configure(config):
    """pytest配置"""
    # 添加自定义标记
    config.addinivalue_line(
        "markers", "smoke: 冒烟测试"
    )
    config.addinivalue_line(
        "markers", "regression: 回归测试"
    )
    config.addinivalue_line(
        "markers", "slow: 慢速测试"
    )


def pytest_collection_modifyitems(config, items):
    """修改测试项"""
    # 为没有标记的测试添加默认标记
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker(pytest.mark.regression)

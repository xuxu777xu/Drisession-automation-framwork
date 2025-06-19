# DrissionPage 现代化自动化框架

🚀 基于 DrissionPage 4.0+ 的企业级模块化自动化测试框架

## ✨ 特性

- 🏗️ **模块化设计** - 清晰的架构分层，易于维护和扩展
- 🔧 **多驱动支持** - 支持 ChromiumPage、SessionPage、WebPage 三种模式
- ⚙️ **智能配置管理** - 支持多环境配置和浏览器预设
- 🎯 **页面对象模式** - 标准的 POM 实现，提高代码复用性
- 📊 **完善的日志系统** - 基于 loguru 的增强日志功能
- 🔄 **等待机制** - 智能等待和重试机制
- 📸 **截图管理** - 自动截图和错误记录
- 🧪 **测试集成** - 与 pytest 无缝集成

## 📁 项目结构

```
drissionpage_framework/
├── config/                 # 配置管理模块
│   ├── __init__.py
│   ├── settings.py         # 全局设置
│   ├── settings.yaml       # 配置文件
│   ├── browser_config.py   # 浏览器配置
│   ├── environment_config.py # 环境配置
│   └── environments/       # 环境配置目录
│       └── test.yaml       # 测试环境配置
├── core/                   # 核心功能模块
│   ├── __init__.py
│   ├── driver_manager.py   # 驱动管理器
│   ├── page_base.py        # 页面基类
│   ├── element_handler.py  # 元素处理器
│   └── wait_handler.py     # 等待处理器
├── pages/                  # 页面对象模块
│   ├── __init__.py
│   ├── base_page.py        # 基础页面类
│   └── example_page.py     # 示例页面
├── utils/                  # 工具模块
│   ├── __init__.py
│   ├── logger.py           # 日志工具
│   ├── data_handler.py     # 数据处理
│   ├── screenshot.py       # 截图管理
│   └── report_generator.py # 报告生成
├── tests/                  # 测试模块
│   ├── __init__.py
│   ├── conftest.py         # pytest配置
│   └── test_example.py     # 示例测试
├── examples/               # 使用示例
│   └── basic_usage.py      # 基础使用示例
├── requirements.txt        # 依赖包
├── pytest.ini            # pytest配置
├── run_tests.py           # 测试运行脚本
└── README.md              # 项目文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 基础使用

```python
from core.driver_manager import driver_manager
from config.browser_config import BrowserPresets
from pages.example_page import ExamplePage

# 创建浏览器配置
config = BrowserPresets.default()

# 创建驱动
driver = driver_manager.create_chromium_page("test", config)

# 创建页面对象
page = ExamplePage(driver)

# 打开页面并执行操作
page.open()
page.search("DrissionPage")
results = page.get_search_results()

# 清理资源
driver_manager.close_driver("test")
```

### 3. 检查环境

```bash
python run_tests.py --check
```

### 4. 运行示例

```bash
python run_tests.py --examples
```

### 5. 运行测试

```bash
# 运行冒烟测试
python run_tests.py --smoke

# 运行所有测试
python run_tests.py --all

# 并行运行测试
python run_tests.py --parallel
```

## 🔧 配置管理

### 浏览器配置

```python
from config.browser_config import BrowserConfig, BrowserPresets

# 使用预设配置
config = BrowserPresets.headless()  # 无头模式
config = BrowserPresets.performance()  # 性能模式
config = BrowserPresets.stealth()  # 隐身模式

# 自定义配置
config = BrowserConfig()
config.set_headless(True)
config.set_window_size(1920, 1080)
config.set_proxy("http://127.0.0.1:8080")
config.disable_images(True)
```

### 环境配置

```python
from config.environment_config import env_manager

# 设置当前环境
env_manager.set_current_environment("test")

# 获取环境配置
env_config = env_manager.get_current_environment()
base_url = env_config.base_url
```

## 🎯 页面对象模式

### 创建页面类

```python
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, driver=None, driver_name="default"):
        super().__init__(driver, driver_name, "https://example.com/login")
    
    def get_page_elements(self):
        return {
            "username_input": "#username",
            "password_input": "#password",
            "login_button": "#login-btn"
        }
    
    def is_loaded(self):
        return self.element_handler.is_displayed(
            self.get_page_elements()["login_button"]
        )
    
    def login(self, username, password):
        elements = self.get_page_elements()
        
        self.element_handler.input_text(elements["username_input"], username)
        self.element_handler.input_text(elements["password_input"], password)
        self.element_handler.click_element(elements["login_button"])
        
        return self.wait_handler.wait_for_url_contains("dashboard")
```

## 🔄 驱动管理

### 多驱动支持

```python
from core.driver_manager import driver_manager

# ChromiumPage - 浏览器控制
chromium_driver = driver_manager.create_chromium_page("browser_test")

# SessionPage - HTTP请求
session_driver = driver_manager.create_session_page("api_test")

# WebPage - 混合模式
web_driver = driver_manager.create_web_page("hybrid_test", mode="d")

# 临时驱动
with driver_manager.get_temp_driver("chromium") as temp_driver:
    # 使用临时驱动
    pass
```

## 📊 日志系统

### 测试日志

```python
from utils.logger import TestLogger

test_logger = TestLogger("登录测试")
test_logger.test_start()

test_logger.step("输入用户名")
test_logger.step("输入密码")
test_logger.step("点击登录按钮")

test_logger.test_end("PASS")
```

### 性能日志

```python
from utils.logger import PerformanceLogger

perf_logger = PerformanceLogger("页面加载")
perf_logger.start_timing("页面加载")
# 执行操作
perf_logger.end_timing("页面加载")
perf_logger.log_memory_usage()
```

## 🧪 测试集成

### 与 pytest 集成

```python
import pytest
from core.driver_manager import driver_manager
from config.browser_config import BrowserPresets

@pytest.fixture
def browser():
    config = BrowserPresets.default()
    driver = driver_manager.create_chromium_page("test", config)
    yield driver
    driver_manager.close_driver("test")

def test_search(browser):
    from pages.example_page import ExamplePage
    
    page = ExamplePage(browser)
    page.open()
    
    assert page.is_loaded()
    assert page.search("DrissionPage")
    
    results = page.get_search_results()
    assert len(results) > 0
```

## 🔧 高级功能

### 等待机制

```python
# 等待元素显示
page.wait_handler.wait_for_element_displayed("#element")

# 等待文本包含
page.wait_handler.wait_for_text_present("成功")

# 等待自定义条件
page.wait_handler.wait_for_condition(
    lambda: len(page.get_search_results()) > 5,
    timeout=10,
    description="搜索结果大于5个"
)
```

### 元素操作

```python
# 基础操作
page.element_handler.click_element("#button")
page.element_handler.input_text("#input", "text")
text = page.element_handler.get_text("#element")

# 高级操作
page.element_handler.hover_element("#menu")
page.element_handler.scroll_to_element("#target")
page.element_handler.get_element_screenshot("#element")
```

## 📈 最佳实践

1. **使用页面对象模式** - 将页面元素和操作封装在页面类中
2. **合理使用等待** - 使用显式等待而不是固定延时
3. **配置管理** - 使用配置文件管理不同环境的设置
4. **日志记录** - 记录关键操作和错误信息
5. **资源清理** - 及时关闭不需要的驱动实例
6. **错误处理** - 使用try-catch处理异常情况

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- [DrissionPage 官方文档](https://drissionpage.cn/)
- [DrissionPage GitHub](https://github.com/g1879/DrissionPage)

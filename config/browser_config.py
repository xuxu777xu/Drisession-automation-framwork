"""
浏览器配置管理
基于DrissionPage 4.0+ ChromiumOptions和SessionOptions
"""

from typing import Dict, List, Optional, Union
from pathlib import Path
from DrissionPage import ChromiumOptions, SessionOptions
from loguru import logger
from .settings import settings


class BrowserConfig:
    """浏览器配置管理器"""
    
    def __init__(self):
        self.chromium_options = ChromiumOptions()
        self.session_options = SessionOptions()
        self._setup_default_config()
    
    def _setup_default_config(self) -> None:
        """设置默认配置"""
        # 基础浏览器配置
        if settings.headless:
            self.chromium_options.headless()
        
        # 设置下载路径
        self.chromium_options.set_paths(
            download_path=str(settings.downloads_dir)
        )
        
        # 禁用一些不必要的功能以提高性能
        self.chromium_options.set_argument('--no-default-browser-check')
        self.chromium_options.set_argument('--disable-suggestions-ui')
        self.chromium_options.set_argument('--no-first-run')
        self.chromium_options.set_argument('--disable-infobars')
        self.chromium_options.set_argument('--disable-popup-blocking')
        
        # 设置用户代理
        self.session_options.set_user_agent(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        logger.info("浏览器默认配置已设置")
    
    def set_headless(self, headless: bool = True) -> "BrowserConfig":
        """设置无头模式"""
        if headless:
            self.chromium_options.headless()
        else:
            # 移除无头模式参数
            self.chromium_options.remove_argument('--headless')
        
        logger.info(f"无头模式设置为: {headless}")
        return self
    
    def set_window_size(self, width: int = 1920, height: int = 1080) -> "BrowserConfig":
        """设置窗口大小"""
        self.chromium_options.set_argument(f'--window-size={width},{height}')
        logger.info(f"窗口大小设置为: {width}x{height}")
        return self
    
    def set_user_data_path(self, path: Union[str, Path]) -> "BrowserConfig":
        """设置用户数据路径"""
        self.chromium_options.set_paths(user_data_path=str(path))
        logger.info(f"用户数据路径设置为: {path}")
        return self
    
    def set_browser_path(self, path: Union[str, Path]) -> "BrowserConfig":
        """设置浏览器可执行文件路径"""
        self.chromium_options.set_paths(browser_path=str(path))
        logger.info(f"浏览器路径设置为: {path}")
        return self
    
    def set_auto_port(self, auto: bool = True) -> "BrowserConfig":
        """设置自动端口分配"""
        if auto:
            self.chromium_options.auto_port()
        logger.info(f"自动端口分配设置为: {auto}")
        return self
    
    def set_proxy(self, proxy: str) -> "BrowserConfig":
        """设置代理"""
        # 为浏览器设置代理
        self.chromium_options.set_argument(f'--proxy-server={proxy}')
        
        # 为Session设置代理
        if proxy.startswith('http://'):
            self.session_options.set_proxies(http=proxy, https=proxy)
        elif proxy.startswith('socks'):
            self.session_options.set_proxies(http=proxy, https=proxy)
        
        logger.info(f"代理设置为: {proxy}")
        return self
    
    def disable_images(self, disable: bool = True) -> "BrowserConfig":
        """禁用图片加载"""
        if disable:
            self.chromium_options.no_imgs()
        logger.info(f"图片加载禁用: {disable}")
        return self
    
    def set_load_strategy(self, strategy: str = "normal") -> "BrowserConfig":
        """设置页面加载策略
        
        Args:
            strategy: 'normal', 'eager', 'none'
        """
        self.chromium_options.set_load_mode(strategy)
        logger.info(f"页面加载策略设置为: {strategy}")
        return self
    
    def add_extension(self, extension_path: Union[str, Path]) -> "BrowserConfig":
        """添加浏览器扩展"""
        self.chromium_options.add_extension(str(extension_path))
        logger.info(f"添加扩展: {extension_path}")
        return self
    
    def set_preferences(self, prefs: Dict) -> "BrowserConfig":
        """设置浏览器首选项"""
        for key, value in prefs.items():
            self.chromium_options.set_pref(key, value)
        logger.info(f"设置浏览器首选项: {prefs}")
        return self
    
    def set_session_headers(self, headers: Dict[str, str]) -> "BrowserConfig":
        """设置Session请求头"""
        self.session_options.set_headers(headers)
        logger.info(f"设置Session请求头: {headers}")
        return self
    
    def set_session_cookies(self, cookies: List[str]) -> "BrowserConfig":
        """设置Session cookies"""
        self.session_options.set_cookies(cookies)
        logger.info(f"设置Session cookies: {len(cookies)}个")
        return self
    
    def set_timeout(self, timeout: int) -> "BrowserConfig":
        """设置超时时间"""
        self.chromium_options.set_timeouts(
            base=timeout,
            page_load=timeout * 3,
            script=timeout * 2
        )
        logger.info(f"超时时间设置为: {timeout}秒")
        return self
    
    def enable_performance_mode(self) -> "BrowserConfig":
        """启用性能模式"""
        # 禁用图片
        self.disable_images()
        
        # 禁用CSS
        self.chromium_options.set_argument('--disable-web-security')
        
        # 禁用JavaScript（可选）
        self.chromium_options.set_argument('--disable-javascript')
        
        # 设置快速加载策略
        self.set_load_strategy('none')
        
        logger.info("性能模式已启用")
        return self
    
    def enable_stealth_mode(self) -> "BrowserConfig":
        """启用隐身模式"""
        # 禁用自动化检测
        self.chromium_options.set_argument('--disable-blink-features=AutomationControlled')
        self.chromium_options.set_argument('--disable-dev-shm-usage')
        self.chromium_options.set_argument('--no-sandbox')
        
        # 设置更真实的用户代理
        self.session_options.set_user_agent(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # 设置更多真实的请求头
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.set_session_headers(headers)
        
        logger.info("隐身模式已启用")
        return self
    
    def save_config(self, config_path: Optional[Path] = None) -> None:
        """保存配置到ini文件"""
        if config_path:
            self.chromium_options.save(str(config_path))
        else:
            self.chromium_options.save()
        logger.info("浏览器配置已保存")
    
    def get_chromium_options(self) -> ChromiumOptions:
        """获取ChromiumOptions对象"""
        return self.chromium_options
    
    def get_session_options(self) -> SessionOptions:
        """获取SessionOptions对象"""
        return self.session_options


# 预定义配置
class BrowserPresets:
    """浏览器预设配置"""
    
    @staticmethod
    def default() -> BrowserConfig:
        """默认配置"""
        return BrowserConfig()
    
    @staticmethod
    def headless() -> BrowserConfig:
        """无头模式配置"""
        return BrowserConfig().set_headless(True)
    
    @staticmethod
    def performance() -> BrowserConfig:
        """性能优化配置"""
        return BrowserConfig().enable_performance_mode()
    
    @staticmethod
    def stealth() -> BrowserConfig:
        """隐身模式配置"""
        return BrowserConfig().enable_stealth_mode()
    
    @staticmethod
    def mobile() -> BrowserConfig:
        """移动端模拟配置"""
        config = BrowserConfig()
        
        # 设置移动端用户代理
        mobile_ua = (
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) '
            'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1'
        )
        config.session_options.set_user_agent(mobile_ua)
        
        # 设置移动端窗口大小
        config.set_window_size(375, 812)
        
        # 设置移动端设备模拟
        config.chromium_options.set_argument('--user-agent=' + mobile_ua)
        
        logger.info("移动端模拟配置已设置")
        return config

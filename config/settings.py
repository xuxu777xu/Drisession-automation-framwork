"""
全局设置管理
基于最新DrissionPage 4.0+ API设计
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import yaml
from loguru import logger


class Settings(BaseModel):
    """全局设置类"""
    
    # 项目路径配置
    project_root: Path = Field(default_factory=lambda: Path.cwd())
    config_dir: Path = Field(default_factory=lambda: Path.cwd() / "config")
    data_dir: Path = Field(default_factory=lambda: Path.cwd() / "data")
    reports_dir: Path = Field(default_factory=lambda: Path.cwd() / "reports")
    logs_dir: Path = Field(default_factory=lambda: Path.cwd() / "logs")
    screenshots_dir: Path = Field(default_factory=lambda: Path.cwd() / "screenshots")
    downloads_dir: Path = Field(default_factory=lambda: Path.cwd() / "downloads")
    
    # 测试配置
    test_timeout: int = Field(default=30, description="默认测试超时时间(秒)")
    element_timeout: int = Field(default=10, description="元素查找超时时间(秒)")
    page_load_timeout: int = Field(default=30, description="页面加载超时时间(秒)")
    
    # 重试配置
    retry_times: int = Field(default=3, description="默认重试次数")
    retry_interval: float = Field(default=2.0, description="重试间隔(秒)")
    
    # 日志配置
    log_level: str = Field(default="INFO", description="日志级别")
    log_format: str = Field(
        default="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        description="日志格式"
    )
    
    # 环境配置
    environment: str = Field(default="test", description="运行环境")
    debug_mode: bool = Field(default=False, description="调试模式")
    
    # 浏览器配置
    headless: bool = Field(default=False, description="无头模式")
    auto_close_browser: bool = Field(default=True, description="自动关闭浏览器")
    
    class Config:
        """Pydantic配置"""
        arbitrary_types_allowed = True
        
    def __init__(self, **data):
        super().__init__(**data)
        self._ensure_directories()
        self._setup_logging()
    
    def _ensure_directories(self) -> None:
        """确保必要的目录存在"""
        directories = [
            self.data_dir,
            self.reports_dir,
            self.logs_dir,
            self.screenshots_dir,
            self.downloads_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _setup_logging(self) -> None:
        """设置日志配置"""
        logger.remove()  # 移除默认处理器
        
        # 控制台日志
        logger.add(
            sink=lambda msg: print(msg, end=""),
            level=self.log_level,
            format=self.log_format,
            colorize=True
        )
        
        # 文件日志
        log_file = self.logs_dir / "automation.log"
        logger.add(
            sink=str(log_file),
            level=self.log_level,
            format=self.log_format,
            rotation="1 day",
            retention="7 days",
            encoding="utf-8"
        )
    
    @classmethod
    def from_yaml(cls, config_path: Optional[Path] = None) -> "Settings":
        """从YAML文件加载配置"""
        if config_path is None:
            config_path = Path.cwd() / "config" / "settings.yaml"
        
        if not config_path.exists():
            logger.warning(f"配置文件不存在: {config_path}, 使用默认配置")
            return cls()
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            logger.info(f"从配置文件加载设置: {config_path}")
            return cls(**config_data)
        
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}, 使用默认配置")
            return cls()
    
    def save_to_yaml(self, config_path: Optional[Path] = None) -> None:
        """保存配置到YAML文件"""
        if config_path is None:
            config_path = self.config_dir / "settings.yaml"
        
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 转换Path对象为字符串以便序列化
        config_dict = self.dict()
        for key, value in config_dict.items():
            if isinstance(value, Path):
                config_dict[key] = str(value)
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True)
            
            logger.info(f"配置已保存到: {config_path}")
        
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
    
    def get_env_config(self) -> Dict[str, Any]:
        """获取环境相关配置"""
        return {
            "environment": self.environment,
            "debug_mode": self.debug_mode,
            "log_level": self.log_level
        }
    
    def update_from_env(self) -> None:
        """从环境变量更新配置"""
        env_mappings = {
            "AUTOMATION_ENV": "environment",
            "AUTOMATION_DEBUG": "debug_mode",
            "AUTOMATION_LOG_LEVEL": "log_level",
            "AUTOMATION_HEADLESS": "headless",
            "AUTOMATION_TIMEOUT": "test_timeout"
        }
        
        for env_var, setting_key in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                # 类型转换
                if setting_key in ["debug_mode", "headless"]:
                    env_value = env_value.lower() in ["true", "1", "yes"]
                elif setting_key in ["test_timeout"]:
                    env_value = int(env_value)
                
                setattr(self, setting_key, env_value)
                logger.info(f"从环境变量更新配置: {setting_key} = {env_value}")


# 全局设置实例
settings = Settings.from_yaml()

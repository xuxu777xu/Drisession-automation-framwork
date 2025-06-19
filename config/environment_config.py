"""
环境配置管理
支持多环境配置（开发、测试、生产等）
"""

from typing import Dict, Any, Optional
from pathlib import Path
from pydantic import BaseModel, Field
import yaml
from loguru import logger


class EnvironmentConfig(BaseModel):
    """环境配置类"""
    
    # 环境基本信息
    name: str = Field(..., description="环境名称")
    description: str = Field(default="", description="环境描述")
    
    # 基础URL配置
    base_url: str = Field(..., description="基础URL")
    api_base_url: Optional[str] = Field(default=None, description="API基础URL")
    
    # 数据库配置
    database: Optional[Dict[str, Any]] = Field(default=None, description="数据库配置")
    
    # 认证配置
    auth: Optional[Dict[str, Any]] = Field(default=None, description="认证配置")
    
    # 第三方服务配置
    services: Optional[Dict[str, Any]] = Field(default=None, description="第三方服务配置")
    
    # 测试数据配置
    test_data: Optional[Dict[str, Any]] = Field(default=None, description="测试数据配置")
    
    # 超时配置
    timeouts: Dict[str, int] = Field(
        default_factory=lambda: {
            "page_load": 30,
            "element_wait": 10,
            "api_request": 30
        },
        description="超时配置"
    )
    
    # 重试配置
    retry: Dict[str, int] = Field(
        default_factory=lambda: {
            "times": 3,
            "interval": 2
        },
        description="重试配置"
    )
    
    # 环境特定的浏览器配置
    browser: Optional[Dict[str, Any]] = Field(default=None, description="浏览器配置")
    
    class Config:
        """Pydantic配置"""
        arbitrary_types_allowed = True


class EnvironmentManager:
    """环境管理器"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.cwd() / "config" / "environments"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._environments: Dict[str, EnvironmentConfig] = {}
        self._current_env: Optional[str] = None
        self._load_environments()
    
    def _load_environments(self) -> None:
        """加载所有环境配置"""
        if not self.config_dir.exists():
            logger.warning(f"环境配置目录不存在: {self.config_dir}")
            return
        
        for config_file in self.config_dir.glob("*.yaml"):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
                
                env_name = config_file.stem
                self._environments[env_name] = EnvironmentConfig(**config_data)
                logger.info(f"加载环境配置: {env_name}")
                
            except Exception as e:
                logger.error(f"加载环境配置失败 {config_file}: {e}")
    
    def add_environment(self, env_config: EnvironmentConfig) -> None:
        """添加环境配置"""
        self._environments[env_config.name] = env_config
        logger.info(f"添加环境配置: {env_config.name}")
    
    def get_environment(self, name: str) -> Optional[EnvironmentConfig]:
        """获取环境配置"""
        return self._environments.get(name)
    
    def list_environments(self) -> List[str]:
        """列出所有环境"""
        return list(self._environments.keys())
    
    def set_current_environment(self, name: str) -> None:
        """设置当前环境"""
        if name not in self._environments:
            raise ValueError(f"环境不存在: {name}")
        
        self._current_env = name
        logger.info(f"当前环境设置为: {name}")
    
    def get_current_environment(self) -> Optional[EnvironmentConfig]:
        """获取当前环境配置"""
        if self._current_env:
            return self._environments.get(self._current_env)
        return None
    
    def save_environment(self, env_config: EnvironmentConfig) -> None:
        """保存环境配置到文件"""
        config_file = self.config_dir / f"{env_config.name}.yaml"
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(
                    env_config.dict(),
                    f,
                    default_flow_style=False,
                    allow_unicode=True
                )
            
            logger.info(f"环境配置已保存: {config_file}")
            
        except Exception as e:
            logger.error(f"保存环境配置失败: {e}")
    
    def create_default_environments(self) -> None:
        """创建默认环境配置"""
        # 开发环境
        dev_config = EnvironmentConfig(
            name="development",
            description="开发环境",
            base_url="http://localhost:3000",
            api_base_url="http://localhost:3000/api",
            auth={
                "username": "dev_user",
                "password": "dev_password"
            },
            test_data={
                "users": [
                    {"username": "test_user1", "password": "password123"},
                    {"username": "test_user2", "password": "password456"}
                ]
            },
            browser={
                "headless": False,
                "window_size": {"width": 1920, "height": 1080}
            }
        )
        
        # 测试环境
        test_config = EnvironmentConfig(
            name="test",
            description="测试环境",
            base_url="https://test.example.com",
            api_base_url="https://test.example.com/api",
            auth={
                "username": "test_user",
                "password": "test_password"
            },
            test_data={
                "users": [
                    {"username": "test_user1", "password": "test123"},
                    {"username": "test_user2", "password": "test456"}
                ]
            },
            browser={
                "headless": True,
                "window_size": {"width": 1920, "height": 1080}
            }
        )
        
        # 生产环境
        prod_config = EnvironmentConfig(
            name="production",
            description="生产环境",
            base_url="https://www.example.com",
            api_base_url="https://api.example.com",
            auth={
                "username": "prod_user",
                "password": "prod_password"
            },
            timeouts={
                "page_load": 60,
                "element_wait": 20,
                "api_request": 60
            },
            browser={
                "headless": True,
                "window_size": {"width": 1920, "height": 1080}
            }
        )
        
        # 保存配置
        for config in [dev_config, test_config, prod_config]:
            self.add_environment(config)
            self.save_environment(config)
        
        logger.info("默认环境配置已创建")


# 全局环境管理器实例
env_manager = EnvironmentManager()

# 如果没有环境配置，创建默认配置
if not env_manager.list_environments():
    env_manager.create_default_environments()

# 设置默认环境
if env_manager.list_environments() and not env_manager.get_current_environment():
    env_manager.set_current_environment("test")

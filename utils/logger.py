"""
日志管理工具
基于loguru的增强日志功能
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any
from loguru import logger
from config import settings


def setup_logger(
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
    rotation: str = "1 day",
    retention: str = "7 days",
    format_string: Optional[str] = None
) -> None:
    """设置日志配置
    
    Args:
        log_level: 日志级别
        log_file: 日志文件路径
        rotation: 日志轮转规则
        retention: 日志保留时间
        format_string: 日志格式
    """
    # 移除默认处理器
    logger.remove()
    
    # 设置格式
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
    
    # 控制台输出
    logger.add(
        sys.stdout,
        level=log_level,
        format=format_string,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # 文件输出
    if log_file is None:
        log_file = settings.logs_dir / "automation.log"
    
    logger.add(
        str(log_file),
        level=log_level,
        format=format_string,
        rotation=rotation,
        retention=retention,
        encoding="utf-8",
        backtrace=True,
        diagnose=True
    )
    
    logger.info(f"日志系统已初始化: {log_file}")


def get_logger(name: str) -> "logger":
    """获取指定名称的日志器
    
    Args:
        name: 日志器名称
        
    Returns:
        日志器实例
    """
    return logger.bind(name=name)


class LoggerMixin:
    """日志混入类 - 为其他类提供日志功能"""
    
    @property
    def logger(self):
        """获取当前类的日志器"""
        return get_logger(self.__class__.__name__)


class TestLogger:
    """测试专用日志器"""
    
    def __init__(self, test_name: str):
        self.test_name = test_name
        self.logger = get_logger(f"TEST.{test_name}")
        self.steps = []
        self.current_step = 0
    
    def step(self, description: str) -> None:
        """记录测试步骤
        
        Args:
            description: 步骤描述
        """
        self.current_step += 1
        step_info = f"步骤 {self.current_step}: {description}"
        self.steps.append(step_info)
        self.logger.info(step_info)
    
    def info(self, message: str) -> None:
        """记录信息"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """记录警告"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """记录错误"""
        self.logger.error(message)
    
    def success(self, message: str) -> None:
        """记录成功"""
        self.logger.success(message)
    
    def debug(self, message: str) -> None:
        """记录调试信息"""
        self.logger.debug(message)
    
    def test_start(self) -> None:
        """测试开始"""
        self.logger.info(f"🚀 测试开始: {self.test_name}")
    
    def test_end(self, result: str = "PASS") -> None:
        """测试结束
        
        Args:
            result: 测试结果 (PASS/FAIL)
        """
        if result == "PASS":
            self.logger.success(f"✅ 测试通过: {self.test_name}")
        else:
            self.logger.error(f"❌ 测试失败: {self.test_name}")
    
    def get_test_summary(self) -> Dict[str, Any]:
        """获取测试摘要
        
        Returns:
            测试摘要信息
        """
        return {
            "test_name": self.test_name,
            "total_steps": len(self.steps),
            "steps": self.steps
        }


class PerformanceLogger:
    """性能日志器"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(f"PERF.{name}")
        self.timings = {}
        self.start_times = {}
    
    def start_timing(self, operation: str) -> None:
        """开始计时
        
        Args:
            operation: 操作名称
        """
        import time
        self.start_times[operation] = time.time()
        self.logger.debug(f"⏱️ 开始计时: {operation}")
    
    def end_timing(self, operation: str) -> float:
        """结束计时
        
        Args:
            operation: 操作名称
            
        Returns:
            耗时（秒）
        """
        import time
        if operation not in self.start_times:
            self.logger.warning(f"未找到操作的开始时间: {operation}")
            return 0.0
        
        duration = time.time() - self.start_times[operation]
        self.timings[operation] = duration
        
        self.logger.info(f"⏱️ {operation} 耗时: {duration:.3f}秒")
        return duration
    
    def log_memory_usage(self) -> None:
        """记录内存使用情况"""
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            
            self.logger.info(
                f"💾 内存使用: RSS={memory_info.rss / 1024 / 1024:.2f}MB, "
                f"VMS={memory_info.vms / 1024 / 1024:.2f}MB"
            )
        except ImportError:
            self.logger.warning("psutil未安装，无法获取内存信息")
        except Exception as e:
            self.logger.error(f"获取内存信息失败: {e}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """获取性能摘要
        
        Returns:
            性能摘要信息
        """
        return {
            "name": self.name,
            "timings": self.timings,
            "total_operations": len(self.timings),
            "total_time": sum(self.timings.values())
        }


# 初始化默认日志配置
setup_logger(
    log_level=settings.log_level,
    log_file=settings.logs_dir / "automation.log"
)

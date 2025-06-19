#!/usr/bin/env python3
"""
测试运行脚本
提供便捷的测试执行入口
"""

import sys
import argparse
from pathlib import Path
import subprocess

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_smoke_tests():
    """运行冒烟测试"""
    print("🔥 运行冒烟测试...")
    cmd = ["python", "-m", "pytest", "-m", "smoke", "-v"]
    return subprocess.run(cmd, cwd=project_root).returncode


def run_regression_tests():
    """运行回归测试"""
    print("🔄 运行回归测试...")
    cmd = ["python", "-m", "pytest", "-m", "regression", "-v"]
    return subprocess.run(cmd, cwd=project_root).returncode


def run_all_tests():
    """运行所有测试"""
    print("🚀 运行所有测试...")
    cmd = ["python", "-m", "pytest", "-v"]
    return subprocess.run(cmd, cwd=project_root).returncode


def run_parallel_tests():
    """并行运行测试"""
    print("⚡ 并行运行测试...")
    cmd = ["python", "-m", "pytest", "-n", "auto", "-v"]
    return subprocess.run(cmd, cwd=project_root).returncode


def run_specific_test(test_path):
    """运行指定测试"""
    print(f"🎯 运行指定测试: {test_path}")
    cmd = ["python", "-m", "pytest", test_path, "-v"]
    return subprocess.run(cmd, cwd=project_root).returncode


def run_examples():
    """运行示例"""
    print("📚 运行框架示例...")
    example_script = project_root / "examples" / "basic_usage.py"
    cmd = ["python", str(example_script)]
    return subprocess.run(cmd, cwd=project_root).returncode


def install_dependencies():
    """安装依赖"""
    print("📦 安装项目依赖...")
    cmd = ["pip", "install", "-r", "requirements.txt"]
    return subprocess.run(cmd, cwd=project_root).returncode


def check_environment():
    """检查环境"""
    print("🔍 检查环境配置...")
    
    try:
        # 检查Python版本
        python_version = sys.version_info
        print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version < (3, 8):
            print("❌ Python版本过低，建议使用Python 3.8+")
            return False
        
        # 检查关键依赖
        required_packages = [
            "DrissionPage",
            "pytest", 
            "loguru",
            "pydantic",
            "PyYAML"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.lower().replace("-", "_"))
                print(f"✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package} (未安装)")
        
        if missing_packages:
            print(f"\n缺少依赖包: {', '.join(missing_packages)}")
            print("请运行: python run_tests.py --install")
            return False
        
        # 检查目录结构
        required_dirs = ["config", "core", "pages", "utils", "tests", "examples"]
        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            if dir_path.exists():
                print(f"✅ {dir_name}/ 目录")
            else:
                print(f"❌ {dir_name}/ 目录缺失")
                return False
        
        print("\n✅ 环境检查通过！")
        return True
        
    except Exception as e:
        print(f"❌ 环境检查失败: {e}")
        return False


def show_help():
    """显示帮助信息"""
    help_text = """
🚀 DrissionPage自动化框架 - 测试运行脚本

用法:
    python run_tests.py [选项]

选项:
    --smoke         运行冒烟测试
    --regression    运行回归测试
    --all           运行所有测试
    --parallel      并行运行测试
    --test PATH     运行指定测试文件或目录
    --examples      运行框架示例
    --install       安装项目依赖
    --check         检查环境配置
    --help          显示此帮助信息

示例:
    python run_tests.py --smoke                    # 运行冒烟测试
    python run_tests.py --test tests/test_example.py  # 运行指定测试
    python run_tests.py --parallel                 # 并行运行所有测试
    python run_tests.py --examples                 # 运行示例代码
    python run_tests.py --check                    # 检查环境

标记说明:
    smoke       - 冒烟测试，快速验证核心功能
    regression  - 回归测试，全面功能验证
    slow        - 慢速测试，执行时间较长
    integration - 集成测试
    unit        - 单元测试

报告位置:
    HTML报告: reports/pytest_report.html
    JSON报告: reports/test_report_*.json
    日志文件: logs/automation.log
    """
    print(help_text)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="DrissionPage自动化框架测试运行脚本",
        add_help=False
    )
    
    parser.add_argument("--smoke", action="store_true", help="运行冒烟测试")
    parser.add_argument("--regression", action="store_true", help="运行回归测试")
    parser.add_argument("--all", action="store_true", help="运行所有测试")
    parser.add_argument("--parallel", action="store_true", help="并行运行测试")
    parser.add_argument("--test", type=str, help="运行指定测试")
    parser.add_argument("--examples", action="store_true", help="运行框架示例")
    parser.add_argument("--install", action="store_true", help="安装项目依赖")
    parser.add_argument("--check", action="store_true", help="检查环境配置")
    parser.add_argument("--help", action="store_true", help="显示帮助信息")
    
    args = parser.parse_args()
    
    # 如果没有参数或者请求帮助，显示帮助信息
    if len(sys.argv) == 1 or args.help:
        show_help()
        return 0
    
    exit_code = 0
    
    try:
        if args.check:
            if not check_environment():
                exit_code = 1
        
        elif args.install:
            exit_code = install_dependencies()
        
        elif args.examples:
            exit_code = run_examples()
        
        elif args.smoke:
            exit_code = run_smoke_tests()
        
        elif args.regression:
            exit_code = run_regression_tests()
        
        elif args.parallel:
            exit_code = run_parallel_tests()
        
        elif args.test:
            exit_code = run_specific_test(args.test)
        
        elif args.all:
            exit_code = run_all_tests()
        
        else:
            print("❌ 未知选项，使用 --help 查看帮助")
            exit_code = 1
    
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断执行")
        exit_code = 1
    
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        exit_code = 1
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())

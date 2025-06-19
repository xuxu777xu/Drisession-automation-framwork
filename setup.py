#!/usr/bin/env python3
"""
DrissionPage自动化框架安装脚本
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README文件
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# 读取requirements文件
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text(encoding="utf-8").strip().split("\n")
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("#")]

setup(
    name="drissionpage-automation-framework",
    version="1.0.0",
    description="基于DrissionPage 4.0+的企业级模块化自动化测试框架",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DrissionPage Framework Team",
    author_email="framework@example.com",
    url="https://github.com/example/drissionpage-framework",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "config": ["*.yaml", "environments/*.yaml"],
        "": ["*.md", "*.txt", "*.ini"],
    },
    install_requires=requirements,
    extras_require={
        "dev": [
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "pytest-cov>=4.0.0",
        ],
        "reporting": [
            "allure-pytest>=2.12.0",
            "pytest-html>=3.1.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
    ],
    keywords="automation testing drissionpage selenium web-automation",
    entry_points={
        "console_scripts": [
            "dp-framework=run_tests:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/example/drissionpage-framework/issues",
        "Source": "https://github.com/example/drissionpage-framework",
        "Documentation": "https://github.com/example/drissionpage-framework/wiki",
    },
)

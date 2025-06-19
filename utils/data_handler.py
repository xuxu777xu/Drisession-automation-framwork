"""
数据处理工具
提供测试数据管理和处理功能
"""

import json
import csv
import yaml
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from loguru import logger
from config import settings


class DataHandler:
    """数据处理器"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """初始化数据处理器
        
        Args:
            data_dir: 数据目录路径
        """
        self.data_dir = data_dir or settings.data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """加载JSON文件
        
        Args:
            filename: 文件名
            
        Returns:
            JSON数据
        """
        file_path = self.data_dir / filename
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"JSON文件加载成功: {file_path}")
            return data
        except Exception as e:
            logger.error(f"JSON文件加载失败 {file_path}: {e}")
            return {}
    
    def save_json(self, data: Dict[str, Any], filename: str) -> bool:
        """保存JSON文件
        
        Args:
            data: 要保存的数据
            filename: 文件名
            
        Returns:
            是否保存成功
        """
        file_path = self.data_dir / filename
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"JSON文件保存成功: {file_path}")
            return True
        except Exception as e:
            logger.error(f"JSON文件保存失败 {file_path}: {e}")
            return False
    
    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """加载YAML文件
        
        Args:
            filename: 文件名
            
        Returns:
            YAML数据
        """
        file_path = self.data_dir / filename
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            logger.info(f"YAML文件加载成功: {file_path}")
            return data or {}
        except Exception as e:
            logger.error(f"YAML文件加载失败 {file_path}: {e}")
            return {}
    
    def save_yaml(self, data: Dict[str, Any], filename: str) -> bool:
        """保存YAML文件
        
        Args:
            data: 要保存的数据
            filename: 文件名
            
        Returns:
            是否保存成功
        """
        file_path = self.data_dir / filename
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            logger.info(f"YAML文件保存成功: {file_path}")
            return True
        except Exception as e:
            logger.error(f"YAML文件保存失败 {file_path}: {e}")
            return False
    
    def load_csv(self, filename: str) -> List[Dict[str, Any]]:
        """加载CSV文件
        
        Args:
            filename: 文件名
            
        Returns:
            CSV数据列表
        """
        file_path = self.data_dir / filename
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            logger.info(f"CSV文件加载成功: {file_path}, 共{len(data)}行")
            return data
        except Exception as e:
            logger.error(f"CSV文件加载失败 {file_path}: {e}")
            return []
    
    def save_csv(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """保存CSV文件
        
        Args:
            data: 要保存的数据
            filename: 文件名
            
        Returns:
            是否保存成功
        """
        if not data:
            logger.warning("数据为空，无法保存CSV文件")
            return False
        
        file_path = self.data_dir / filename
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            logger.info(f"CSV文件保存成功: {file_path}, 共{len(data)}行")
            return True
        except Exception as e:
            logger.error(f"CSV文件保存失败 {file_path}: {e}")
            return False
    
    def load_excel(self, filename: str, sheet_name: str = None) -> List[Dict[str, Any]]:
        """加载Excel文件
        
        Args:
            filename: 文件名
            sheet_name: 工作表名称
            
        Returns:
            Excel数据列表
        """
        file_path = self.data_dir / filename
        
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            data = df.to_dict('records')
            logger.info(f"Excel文件加载成功: {file_path}, 共{len(data)}行")
            return data
        except Exception as e:
            logger.error(f"Excel文件加载失败 {file_path}: {e}")
            return []
    
    def save_excel(self, data: List[Dict[str, Any]], filename: str, sheet_name: str = 'Sheet1') -> bool:
        """保存Excel文件
        
        Args:
            data: 要保存的数据
            filename: 文件名
            sheet_name: 工作表名称
            
        Returns:
            是否保存成功
        """
        if not data:
            logger.warning("数据为空，无法保存Excel文件")
            return False
        
        file_path = self.data_dir / filename
        
        try:
            df = pd.DataFrame(data)
            df.to_excel(file_path, sheet_name=sheet_name, index=False)
            logger.info(f"Excel文件保存成功: {file_path}, 共{len(data)}行")
            return True
        except Exception as e:
            logger.error(f"Excel文件保存失败 {file_path}: {e}")
            return False
    
    def generate_test_data(self, template: Dict[str, Any], count: int = 10) -> List[Dict[str, Any]]:
        """生成测试数据
        
        Args:
            template: 数据模板
            count: 生成数量
            
        Returns:
            生成的测试数据列表
        """
        try:
            from faker import Faker
            fake = Faker('zh_CN')
            
            test_data = []
            for i in range(count):
                data_item = {}
                for key, value_type in template.items():
                    if value_type == 'name':
                        data_item[key] = fake.name()
                    elif value_type == 'email':
                        data_item[key] = fake.email()
                    elif value_type == 'phone':
                        data_item[key] = fake.phone_number()
                    elif value_type == 'address':
                        data_item[key] = fake.address()
                    elif value_type == 'company':
                        data_item[key] = fake.company()
                    elif value_type == 'text':
                        data_item[key] = fake.text(max_nb_chars=50)
                    elif value_type == 'number':
                        data_item[key] = fake.random_int(min=1, max=1000)
                    elif value_type == 'date':
                        data_item[key] = fake.date()
                    else:
                        data_item[key] = str(value_type)
                
                test_data.append(data_item)
            
            logger.info(f"测试数据生成成功: {count}条")
            return test_data
            
        except ImportError:
            logger.error("Faker库未安装，无法生成测试数据")
            return []
        except Exception as e:
            logger.error(f"生成测试数据失败: {e}")
            return []
    
    def filter_data(self, data: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """过滤数据
        
        Args:
            data: 原始数据
            filters: 过滤条件
            
        Returns:
            过滤后的数据
        """
        try:
            filtered_data = []
            for item in data:
                match = True
                for key, value in filters.items():
                    if key not in item or item[key] != value:
                        match = False
                        break
                if match:
                    filtered_data.append(item)
            
            logger.info(f"数据过滤完成: {len(data)} -> {len(filtered_data)}")
            return filtered_data
            
        except Exception as e:
            logger.error(f"数据过滤失败: {e}")
            return data
    
    def merge_data(self, *data_lists: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """合并多个数据列表
        
        Args:
            *data_lists: 多个数据列表
            
        Returns:
            合并后的数据列表
        """
        try:
            merged_data = []
            for data_list in data_lists:
                merged_data.extend(data_list)
            
            logger.info(f"数据合并完成: 共{len(merged_data)}条")
            return merged_data
            
        except Exception as e:
            logger.error(f"数据合并失败: {e}")
            return []


# 全局数据处理器实例
data_handler = DataHandler()

"""
截图管理工具
提供截图功能和管理
"""

import time
from pathlib import Path
from typing import Optional, Union, List
from PIL import Image, ImageDraw, ImageFont
from loguru import logger
from config import settings


class ScreenshotManager:
    """截图管理器"""
    
    def __init__(self, screenshot_dir: Optional[Path] = None):
        """初始化截图管理器
        
        Args:
            screenshot_dir: 截图目录路径
        """
        self.screenshot_dir = screenshot_dir or settings.screenshots_dir
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    def take_screenshot(
        self,
        page_obj,
        filename: Optional[str] = None,
        full_page: bool = True,
        add_timestamp: bool = True
    ) -> str:
        """截图
        
        Args:
            page_obj: 页面对象
            filename: 文件名
            full_page: 是否全页截图
            add_timestamp: 是否添加时间戳
            
        Returns:
            截图文件路径
        """
        if filename is None:
            timestamp = int(time.time())
            filename = f"screenshot_{timestamp}.png"
        elif add_timestamp:
            timestamp = int(time.time())
            name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, 'png')
            filename = f"{name}_{timestamp}.{ext}"
        
        screenshot_path = self.screenshot_dir / filename
        
        try:
            if hasattr(page_obj.driver, 'get_screenshot'):
                page_obj.driver.get_screenshot(
                    path=str(self.screenshot_dir),
                    name=filename,
                    full_page=full_page
                )
                logger.info(f"截图已保存: {screenshot_path}")
                return str(screenshot_path)
            else:
                logger.warning("当前驱动不支持截图功能")
                return ""
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return ""
    
    def take_element_screenshot(
        self,
        element,
        filename: Optional[str] = None,
        add_timestamp: bool = True
    ) -> str:
        """元素截图
        
        Args:
            element: 元素对象
            filename: 文件名
            add_timestamp: 是否添加时间戳
            
        Returns:
            截图文件路径
        """
        if filename is None:
            timestamp = int(time.time())
            filename = f"element_{timestamp}.png"
        elif add_timestamp:
            timestamp = int(time.time())
            name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, 'png')
            filename = f"{name}_{timestamp}.{ext}"
        
        screenshot_path = self.screenshot_dir / filename
        
        try:
            if hasattr(element, 'get_screenshot'):
                element.get_screenshot(
                    path=str(self.screenshot_dir),
                    name=filename
                )
                logger.info(f"元素截图已保存: {screenshot_path}")
                return str(screenshot_path)
            else:
                logger.warning("当前元素不支持截图功能")
                return ""
        except Exception as e:
            logger.error(f"元素截图失败: {e}")
            return ""
    
    def add_annotation(
        self,
        image_path: Union[str, Path],
        annotations: List[dict],
        output_path: Optional[Union[str, Path]] = None
    ) -> str:
        """为截图添加注释
        
        Args:
            image_path: 原始图片路径
            annotations: 注释列表，格式: [{"text": "注释", "position": (x, y), "color": "red"}]
            output_path: 输出路径
            
        Returns:
            注释后的图片路径
        """
        try:
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)
            
            # 尝试加载字体
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            for annotation in annotations:
                text = annotation.get("text", "")
                position = annotation.get("position", (10, 10))
                color = annotation.get("color", "red")
                
                # 绘制文本
                draw.text(position, text, fill=color, font=font)
            
            # 保存注释后的图片
            if output_path is None:
                timestamp = int(time.time())
                output_path = self.screenshot_dir / f"annotated_{timestamp}.png"
            
            image.save(output_path)
            logger.info(f"注释截图已保存: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"添加注释失败: {e}")
            return ""
    
    def compare_screenshots(
        self,
        image1_path: Union[str, Path],
        image2_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        threshold: float = 0.1
    ) -> dict:
        """比较两张截图
        
        Args:
            image1_path: 第一张图片路径
            image2_path: 第二张图片路径
            output_path: 差异图输出路径
            threshold: 差异阈值
            
        Returns:
            比较结果字典
        """
        try:
            from PIL import ImageChops
            import numpy as np
            
            image1 = Image.open(image1_path)
            image2 = Image.open(image2_path)
            
            # 确保图片尺寸相同
            if image1.size != image2.size:
                logger.warning("图片尺寸不同，调整为相同尺寸")
                image2 = image2.resize(image1.size)
            
            # 计算差异
            diff = ImageChops.difference(image1, image2)
            
            # 转换为numpy数组计算差异百分比
            diff_array = np.array(diff)
            total_pixels = diff_array.size
            different_pixels = np.count_nonzero(diff_array)
            difference_percentage = (different_pixels / total_pixels) * 100
            
            # 保存差异图
            if output_path is None:
                timestamp = int(time.time())
                output_path = self.screenshot_dir / f"diff_{timestamp}.png"
            
            diff.save(output_path)
            
            result = {
                "difference_percentage": difference_percentage,
                "is_similar": difference_percentage < threshold * 100,
                "diff_image_path": str(output_path),
                "total_pixels": total_pixels,
                "different_pixels": different_pixels
            }
            
            logger.info(f"截图比较完成: 差异 {difference_percentage:.2f}%")
            return result
            
        except Exception as e:
            logger.error(f"截图比较失败: {e}")
            return {"error": str(e)}
    
    def create_screenshot_grid(
        self,
        image_paths: List[Union[str, Path]],
        output_path: Optional[Union[str, Path]] = None,
        grid_size: Optional[tuple] = None
    ) -> str:
        """创建截图网格
        
        Args:
            image_paths: 图片路径列表
            output_path: 输出路径
            grid_size: 网格尺寸 (rows, cols)
            
        Returns:
            网格图片路径
        """
        try:
            if not image_paths:
                logger.warning("图片路径列表为空")
                return ""
            
            # 计算网格尺寸
            if grid_size is None:
                import math
                cols = math.ceil(math.sqrt(len(image_paths)))
                rows = math.ceil(len(image_paths) / cols)
                grid_size = (rows, cols)
            
            rows, cols = grid_size
            
            # 加载第一张图片获取尺寸
            first_image = Image.open(image_paths[0])
            img_width, img_height = first_image.size
            
            # 创建网格画布
            grid_width = cols * img_width
            grid_height = rows * img_height
            grid_image = Image.new('RGB', (grid_width, grid_height), 'white')
            
            # 放置图片
            for i, image_path in enumerate(image_paths):
                if i >= rows * cols:
                    break
                
                row = i // cols
                col = i % cols
                
                image = Image.open(image_path)
                image = image.resize((img_width, img_height))
                
                x = col * img_width
                y = row * img_height
                grid_image.paste(image, (x, y))
            
            # 保存网格图片
            if output_path is None:
                timestamp = int(time.time())
                output_path = self.screenshot_dir / f"grid_{timestamp}.png"
            
            grid_image.save(output_path)
            logger.info(f"截图网格已保存: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"创建截图网格失败: {e}")
            return ""
    
    def cleanup_old_screenshots(self, days: int = 7) -> int:
        """清理旧截图
        
        Args:
            days: 保留天数
            
        Returns:
            删除的文件数量
        """
        try:
            import time
            current_time = time.time()
            cutoff_time = current_time - (days * 24 * 60 * 60)
            
            deleted_count = 0
            for file_path in self.screenshot_dir.glob("*.png"):
                if file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    deleted_count += 1
            
            logger.info(f"清理旧截图完成: 删除 {deleted_count} 个文件")
            return deleted_count
            
        except Exception as e:
            logger.error(f"清理旧截图失败: {e}")
            return 0
    
    def get_screenshot_info(self, image_path: Union[str, Path]) -> dict:
        """获取截图信息
        
        Args:
            image_path: 图片路径
            
        Returns:
            截图信息字典
        """
        try:
            image = Image.open(image_path)
            file_path = Path(image_path)
            
            info = {
                "filename": file_path.name,
                "size": image.size,
                "mode": image.mode,
                "format": image.format,
                "file_size": file_path.stat().st_size,
                "created_time": file_path.stat().st_ctime,
                "modified_time": file_path.stat().st_mtime
            }
            
            return info
            
        except Exception as e:
            logger.error(f"获取截图信息失败: {e}")
            return {}


# 全局截图管理器实例
screenshot_manager = ScreenshotManager()

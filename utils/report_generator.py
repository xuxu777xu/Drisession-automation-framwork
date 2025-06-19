"""
报告生成器
生成测试报告和统计信息
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger
from config import settings


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, reports_dir: Optional[Path] = None):
        """初始化报告生成器
        
        Args:
            reports_dir: 报告目录路径
        """
        self.reports_dir = reports_dir or settings.reports_dir
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.test_results = []
        self.start_time = None
        self.end_time = None
    
    def start_test_session(self) -> None:
        """开始测试会话"""
        self.start_time = datetime.now()
        self.test_results = []
        logger.info("测试会话开始")
    
    def end_test_session(self) -> None:
        """结束测试会话"""
        self.end_time = datetime.now()
        logger.info("测试会话结束")
    
    def add_test_result(self, test_result: Dict[str, Any]) -> None:
        """添加测试结果
        
        Args:
            test_result: 测试结果字典
        """
        test_result['timestamp'] = datetime.now().isoformat()
        self.test_results.append(test_result)
        logger.debug(f"添加测试结果: {test_result.get('name', 'Unknown')}")
    
    def generate_html_report(self, filename: Optional[str] = None) -> str:
        """生成HTML报告
        
        Args:
            filename: 报告文件名
            
        Returns:
            报告文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_report_{timestamp}.html"
        
        report_path = self.reports_dir / filename
        
        try:
            # 计算统计信息
            stats = self._calculate_statistics()
            
            # 生成HTML内容
            html_content = self._generate_html_content(stats)
            
            # 保存HTML文件
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML报告已生成: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"生成HTML报告失败: {e}")
            return ""
    
    def generate_json_report(self, filename: Optional[str] = None) -> str:
        """生成JSON报告
        
        Args:
            filename: 报告文件名
            
        Returns:
            报告文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_report_{timestamp}.json"
        
        report_path = self.reports_dir / filename
        
        try:
            # 计算统计信息
            stats = self._calculate_statistics()
            
            # 构建报告数据
            report_data = {
                "session_info": {
                    "start_time": self.start_time.isoformat() if self.start_time else None,
                    "end_time": self.end_time.isoformat() if self.end_time else None,
                    "duration": stats["duration"]
                },
                "statistics": stats,
                "test_results": self.test_results
            }
            
            # 保存JSON文件
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"JSON报告已生成: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"生成JSON报告失败: {e}")
            return ""
    
    def _calculate_statistics(self) -> Dict[str, Any]:
        """计算统计信息
        
        Returns:
            统计信息字典
        """
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.get('status') == 'PASS')
        failed_tests = sum(1 for result in self.test_results if result.get('status') == 'FAIL')
        skipped_tests = sum(1 for result in self.test_results if result.get('status') == 'SKIP')
        
        # 计算持续时间
        duration = 0
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
        
        # 计算通过率
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "skipped_tests": skipped_tests,
            "pass_rate": round(pass_rate, 2),
            "duration": round(duration, 2)
        }
    
    def _generate_html_content(self, stats: Dict[str, Any]) -> str:
        """生成HTML内容
        
        Args:
            stats: 统计信息
            
        Returns:
            HTML内容
        """
        # HTML模板
        html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DrissionPage自动化测试报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #333; margin-bottom: 10px; }
        .stats { display: flex; justify-content: space-around; margin-bottom: 30px; }
        .stat-card { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; min-width: 120px; }
        .stat-card h3 { margin: 0; font-size: 24px; }
        .stat-card p { margin: 5px 0 0 0; color: #666; }
        .pass { color: #28a745; }
        .fail { color: #dc3545; }
        .skip { color: #ffc107; }
        .results { margin-top: 30px; }
        .result-item { background: #f8f9fa; margin: 10px 0; padding: 15px; border-radius: 5px; border-left: 4px solid #ddd; }
        .result-item.pass { border-left-color: #28a745; }
        .result-item.fail { border-left-color: #dc3545; }
        .result-item.skip { border-left-color: #ffc107; }
        .result-header { display: flex; justify-content: space-between; align-items: center; }
        .result-name { font-weight: bold; }
        .result-status { padding: 4px 8px; border-radius: 4px; color: white; font-size: 12px; }
        .status-pass { background-color: #28a745; }
        .status-fail { background-color: #dc3545; }
        .status-skip { background-color: #ffc107; }
        .result-details { margin-top: 10px; font-size: 14px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 DrissionPage自动化测试报告</h1>
            <p>生成时间: {generation_time}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{total_tests}</h3>
                <p>总测试数</p>
            </div>
            <div class="stat-card">
                <h3 class="pass">{passed_tests}</h3>
                <p>通过</p>
            </div>
            <div class="stat-card">
                <h3 class="fail">{failed_tests}</h3>
                <p>失败</p>
            </div>
            <div class="stat-card">
                <h3 class="skip">{skipped_tests}</h3>
                <p>跳过</p>
            </div>
            <div class="stat-card">
                <h3>{pass_rate}%</h3>
                <p>通过率</p>
            </div>
            <div class="stat-card">
                <h3>{duration}s</h3>
                <p>总耗时</p>
            </div>
        </div>
        
        <div class="results">
            <h2>测试结果详情</h2>
            {test_results_html}
        </div>
    </div>
</body>
</html>
        """
        
        # 生成测试结果HTML
        test_results_html = ""
        for result in self.test_results:
            status = result.get('status', 'UNKNOWN').lower()
            status_class = f"status-{status}" if status in ['pass', 'fail', 'skip'] else "status-unknown"
            
            test_results_html += f"""
            <div class="result-item {status}">
                <div class="result-header">
                    <span class="result-name">{result.get('name', 'Unknown Test')}</span>
                    <span class="result-status {status_class}">{result.get('status', 'UNKNOWN')}</span>
                </div>
                <div class="result-details">
                    <p><strong>描述:</strong> {result.get('description', 'N/A')}</p>
                    <p><strong>耗时:</strong> {result.get('duration', 'N/A')}秒</p>
                    <p><strong>时间:</strong> {result.get('timestamp', 'N/A')}</p>
                    {f'<p><strong>错误信息:</strong> {result.get("error", "")}</p>' if result.get('error') else ''}
                </div>
            </div>
            """
        
        # 填充模板
        return html_template.format(
            generation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_tests=stats["total_tests"],
            passed_tests=stats["passed_tests"],
            failed_tests=stats["failed_tests"],
            skipped_tests=stats["skipped_tests"],
            pass_rate=stats["pass_rate"],
            duration=stats["duration"],
            test_results_html=test_results_html
        )
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """生成摘要报告
        
        Returns:
            摘要报告字典
        """
        stats = self._calculate_statistics()
        
        summary = {
            "session_summary": {
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "end_time": self.end_time.isoformat() if self.end_time else None,
                "duration": stats["duration"]
            },
            "test_summary": stats,
            "failed_tests": [
                result for result in self.test_results 
                if result.get('status') == 'FAIL'
            ],
            "recommendations": self._generate_recommendations(stats)
        }
        
        return summary
    
    def _generate_recommendations(self, stats: Dict[str, Any]) -> List[str]:
        """生成建议
        
        Args:
            stats: 统计信息
            
        Returns:
            建议列表
        """
        recommendations = []
        
        if stats["pass_rate"] < 80:
            recommendations.append("通过率较低，建议检查失败的测试用例")
        
        if stats["failed_tests"] > 0:
            recommendations.append("存在失败的测试用例，建议优先修复")
        
        if stats["duration"] > 300:  # 5分钟
            recommendations.append("测试执行时间较长，建议优化测试用例或使用并行执行")
        
        if stats["total_tests"] < 10:
            recommendations.append("测试用例数量较少，建议增加更多测试覆盖")
        
        return recommendations
    
    def export_to_csv(self, filename: Optional[str] = None) -> str:
        """导出为CSV格式
        
        Args:
            filename: 文件名
            
        Returns:
            CSV文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_results_{timestamp}.csv"
        
        csv_path = self.reports_dir / filename
        
        try:
            import csv
            
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                if self.test_results:
                    fieldnames = self.test_results[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.test_results)
            
            logger.info(f"CSV报告已生成: {csv_path}")
            return str(csv_path)
            
        except Exception as e:
            logger.error(f"生成CSV报告失败: {e}")
            return ""


# 全局报告生成器实例
report_generator = ReportGenerator()

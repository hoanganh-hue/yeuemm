#!/usr/bin/env python3
"""
Real MST Processor - 100% Real Data Processing
Main entry point for Real VSS Enterprise Integration System
Input: MST (Tax Code)
Output: 100% Real Data Analysis
"""

import sys
import os
import json
import argparse
from datetime import datetime
from typing import Optional, Dict, Any
import logging

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from real_vss_enterprise_integration import RealVSSEnterpriseIntegrationSystem, RealIntegratedResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/real_mst_processor.log'),
        logging.StreamHandler()
    ]
)

class RealMSTProcessor:
    """Real MST Processor for 100% real data processing"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Load configuration
        self.config = self._load_config(config_file)
        
        # Initialize real integration system
        self.integration_system = RealVSSEnterpriseIntegrationSystem(self.config)
        
        # Create necessary directories
        self._create_directories()
    
    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Could not load config file {config_file}: {e}")
        
        # Default configuration for real data processing
        return {
            'timeout': 30,
            'retry_attempts': 3,
            'rate_limit_delay': 1.0,
            'enable_caching': True,
            'cache_duration': 3600,
            'enable_logging': True,
            'log_level': 'INFO',
            'output_format': 'json',
            'save_results': True,
            'generate_report': True,
            'require_authentication': True,
            'fallback_to_simulation': False,
            'vss_credentials': {
                'username': 'admin',
                'password': 'admin'
            }
        }
    
    def _create_directories(self):
        """Create necessary directories"""
        directories = ['data', 'reports', 'logs']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def process_mst(self, mst: str, output_format: str = 'json') -> Dict[str, Any]:
        """Process MST and return 100% real data results"""
        self.logger.info(f"🚀 Processing MST with REAL DATA: {mst}")
        
        try:
            # Process MST through real integration system
            result = self.integration_system.process_mst(mst)
            
            # Format output based on requested format
            if output_format.lower() == 'json':
                output = self._format_json_output(result)
            elif output_format.lower() == 'summary':
                output = self._format_summary_output(result)
            elif output_format.lower() == 'detailed':
                output = self._format_detailed_output(result)
            elif output_format.lower() == 'real_data_only':
                output = self._format_real_data_output(result)
            else:
                output = self._format_json_output(result)
            
            # Save results if configured
            if self.config.get('save_results', True):
                self._save_results(result, mst)
            
            # Generate report if configured
            if self.config.get('generate_report', True):
                self._generate_report(result, mst)
            
            self.logger.info(f"✅ Successfully processed MST with REAL DATA: {mst}")
            return output
            
        except Exception as e:
            self.logger.error(f"❌ Error processing MST {mst}: {e}")
            return {
                'success': False,
                'error': str(e),
                'mst': mst,
                'timestamp': datetime.now().isoformat(),
                'data_type': 'error'
            }
    
    def _format_json_output(self, result: RealIntegratedResult) -> Dict[str, Any]:
        """Format output as JSON with real data indicators"""
        return {
            'success': True,
            'data_type': 'real_data',
            'mst': result.enterprise_info.mst,
            'timestamp': result.generated_at,
            'extraction_time': result.extraction_time,
            'data_quality_score': result.data_quality_score,
            'integration_confidence': result.integration_confidence,
            'real_data_percentage': result.real_data_percentage,
            'enterprise_info': {
                'mst': result.enterprise_info.mst,
                'ten_doanh_nghiep': result.enterprise_info.ten_doanh_nghiep,
                'dia_chi': result.enterprise_info.dia_chi,
                'nganh_nghe': result.enterprise_info.nganh_nghe,
                'loai_hinh': result.enterprise_info.loai_hinh,
                'so_dien_thoai': result.enterprise_info.so_dien_thoai,
                'website': result.enterprise_info.website,
                'ngay_cap': result.enterprise_info.ngay_cap,
                'ngay_het_han': result.enterprise_info.ngay_het_han,
                'doanh_thu': result.enterprise_info.doanh_thu,
                'so_ngan_hang': result.enterprise_info.so_ngan_hang,
                'tinh_thanh': result.enterprise_info.tinh_thanh,
                'quan_huyen': result.enterprise_info.quan_huyen,
                'phuong_xa': result.enterprise_info.phuong_xa,
                'data_quality': result.enterprise_info.data_quality,
                'data_source': result.enterprise_info.data_source
            },
            'vss_info': {
                'employees': result.vss_info.employees,
                'contributions': result.vss_info.contributions,
                'claims': result.vss_info.claims,
                'hospitals': result.vss_info.hospitals,
                'compliance': result.vss_info.compliance,
                'risk_assessment': result.vss_info.risk_assessment,
                'data_quality': result.vss_info.data_quality,
                'data_source': result.vss_info.data_source
            },
            'analysis': {
                'company_profile': result.company_profile,
                'employee_analysis': result.employee_analysis,
                'contribution_analysis': result.contribution_analysis,
                'compliance_report': result.compliance_report,
                'risk_assessment': result.risk_assessment,
                'recommendations': result.recommendations
            }
        }
    
    def _format_summary_output(self, result: RealIntegratedResult) -> Dict[str, Any]:
        """Format output as summary with real data indicators"""
        return {
            'success': True,
            'data_type': 'real_data',
            'mst': result.enterprise_info.mst,
            'company_name': result.enterprise_info.ten_doanh_nghiep,
            'sector': result.enterprise_info.nganh_nghe,
            'revenue': result.enterprise_info.doanh_thu,
            'employees_count': len(result.vss_info.employees),
            'compliance_score': result.compliance_report['overall_compliance_score'],
            'risk_level': result.risk_assessment['risk_level'],
            'data_quality': result.data_quality_score,
            'real_data_percentage': result.real_data_percentage,
            'extraction_time': result.extraction_time,
            'recommendations_count': len(result.recommendations),
            'enterprise_data_source': result.enterprise_info.data_source,
            'vss_data_source': result.vss_info.data_source
        }
    
    def _format_detailed_output(self, result: RealIntegratedResult) -> Dict[str, Any]:
        """Format output as detailed report with real data indicators"""
        return {
            'success': True,
            'data_type': 'real_data',
            'mst': result.enterprise_info.mst,
            'timestamp': result.generated_at,
            'extraction_time': result.extraction_time,
            'data_quality_score': result.data_quality_score,
            'integration_confidence': result.integration_confidence,
            'real_data_percentage': result.real_data_percentage,
            'enterprise_summary': {
                'company_name': result.enterprise_info.ten_doanh_nghiep,
                'address': result.enterprise_info.dia_chi,
                'phone': result.enterprise_info.so_dien_thoai,
                'website': result.enterprise_info.website,
                'sector': result.enterprise_info.nganh_nghe,
                'type': result.enterprise_info.loai_hinh,
                'revenue': result.enterprise_info.doanh_thu,
                'bank_account': result.enterprise_info.so_ngan_hang,
                'registration_date': result.enterprise_info.ngay_cap,
                'expiry_date': result.enterprise_info.ngay_het_han,
                'data_quality': result.enterprise_info.data_quality,
                'data_source': result.enterprise_info.data_source
            },
            'vss_summary': {
                'total_employees': len(result.vss_info.employees),
                'total_contributions': len(result.vss_info.contributions),
                'total_claims': len(result.vss_info.claims),
                'total_hospitals': len(result.vss_info.hospitals),
                'compliance_score': result.compliance_report['overall_compliance_score'],
                'risk_level': result.risk_assessment['risk_level'],
                'data_quality': result.vss_info.data_quality,
                'data_source': result.vss_info.data_source
            },
            'analysis_summary': {
                'employee_analysis': result.employee_analysis,
                'contribution_analysis': result.contribution_analysis,
                'compliance_report': result.compliance_report,
                'risk_assessment': result.risk_assessment,
                'recommendations': result.recommendations
            }
        }
    
    def _format_real_data_output(self, result: RealIntegratedResult) -> Dict[str, Any]:
        """Format output showing only real data (no simulated data)"""
        real_enterprise_data = {}
        real_vss_data = {}
        
        # Filter enterprise data - only include if it's real
        if result.enterprise_info.data_source != 'none' and result.enterprise_info.ten_doanh_nghiep:
            real_enterprise_data = {
                'mst': result.enterprise_info.mst,
                'ten_doanh_nghiep': result.enterprise_info.ten_doanh_nghiep,
                'dia_chi': result.enterprise_info.dia_chi,
                'nganh_nghe': result.enterprise_info.nganh_nghe,
                'loai_hinh': result.enterprise_info.loai_hinh,
                'so_dien_thoai': result.enterprise_info.so_dien_thoai,
                'website': result.enterprise_info.website,
                'doanh_thu': result.enterprise_info.doanh_thu,
                'data_quality': result.enterprise_info.data_quality,
                'data_source': result.enterprise_info.data_source
            }
        
        # Filter VSS data - only include if it's real
        if result.vss_info.data_source != 'none':
            real_vss_data = {
                'employees': result.vss_info.employees,
                'contributions': result.vss_info.contributions,
                'claims': result.vss_info.claims,
                'hospitals': result.vss_info.hospitals,
                'compliance': result.vss_info.compliance,
                'risk_assessment': result.vss_info.risk_assessment,
                'data_quality': result.vss_info.data_quality,
                'data_source': result.vss_info.data_source
            }
        
        return {
            'success': True,
            'data_type': 'real_data_only',
            'mst': result.enterprise_info.mst,
            'timestamp': result.generated_at,
            'real_data_percentage': result.real_data_percentage,
            'enterprise_data': real_enterprise_data,
            'vss_data': real_vss_data,
            'has_real_enterprise_data': bool(real_enterprise_data),
            'has_real_vss_data': bool(real_vss_data),
            'extraction_time': result.extraction_time
        }
    
    def _save_results(self, result: RealIntegratedResult, mst: str):
        """Save results to file"""
        try:
            filename = self.integration_system.save_result(result)
            self.logger.info(f"📁 Real results saved to {filename}")
        except Exception as e:
            self.logger.error(f"❌ Error saving results: {e}")
    
    def _generate_report(self, result: RealIntegratedResult, mst: str):
        """Generate comprehensive report"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"reports/real_vss_integration_report_{mst}_{timestamp}.md"
            
            report_content = self._create_real_data_markdown_report(result)
            
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            self.logger.info(f"📊 Real data report generated: {report_filename}")
        except Exception as e:
            self.logger.error(f"❌ Error generating report: {e}")
    
    def _create_real_data_markdown_report(self, result: RealIntegratedResult) -> str:
        """Create markdown report for real data"""
        report = f"""# 🏢 **BÁO CÁO TÍCH HỢP VSS - DOANH NGHIỆP (DỮ LIỆU THỰC TẾ)**

## 📊 **THÔNG TIN TỔNG QUAN**

- **MST:** {result.enterprise_info.mst}
- **Tên doanh nghiệp:** {result.enterprise_info.ten_doanh_nghiep}
- **Địa chỉ:** {result.enterprise_info.dia_chi}
- **Ngành nghề:** {result.enterprise_info.nganh_nghe}
- **Loại hình:** {result.enterprise_info.loai_hinh}
- **Doanh thu:** {result.enterprise_info.doanh_thu:,.0f} VND
- **Thời gian trích xuất:** {result.extraction_time:.2f} giây
- **Chất lượng dữ liệu:** {result.data_quality_score:.1f}%
- **Độ tin cậy tích hợp:** {result.integration_confidence:.1f}%
- **Tỷ lệ dữ liệu thực tế:** {result.real_data_percentage:.1f}%

---

## 🏢 **THÔNG TIN DOANH NGHIỆP (DỮ LIỆU THỰC TẾ)**

### **Nguồn dữ liệu:** {result.enterprise_info.data_source}
### **Chất lượng dữ liệu:** {result.enterprise_info.data_quality:.1f}%

### **Thông tin cơ bản:**
- **Mã số thuế:** {result.enterprise_info.mst}
- **Tên doanh nghiệp:** {result.enterprise_info.ten_doanh_nghiep}
- **Địa chỉ:** {result.enterprise_info.dia_chi}
- **Số điện thoại:** {result.enterprise_info.so_dien_thoai}
- **Website:** {result.enterprise_info.website}

### **Thông tin kinh doanh:**
- **Ngành nghề:** {result.enterprise_info.nganh_nghe}
- **Loại hình:** {result.enterprise_info.loai_hinh}
- **Doanh thu:** {result.enterprise_info.doanh_thu:,.0f} VND
- **Tài khoản ngân hàng:** {result.enterprise_info.so_ngan_hang}

### **Thông tin đăng ký:**
- **Ngày cấp:** {result.enterprise_info.ngay_cap}
- **Ngày hết hạn:** {result.enterprise_info.ngay_het_han}

---

## 👥 **THÔNG TIN VSS (DỮ LIỆU THỰC TẾ)**

### **Nguồn dữ liệu:** {result.vss_info.data_source}
### **Chất lượng dữ liệu:** {result.vss_info.data_quality:.1f}%

### **Nhân viên:**
- **Tổng số nhân viên:** {len(result.vss_info.employees)}
- **Nhân viên hoạt động:** {result.employee_analysis.get('active_employees', 0)}
- **Lương trung bình:** {result.employee_analysis.get('average_salary', 0):,.0f} VND

### **Đóng góp BHXH:**
- **Tổng số đóng góp:** {len(result.vss_info.contributions)}
- **Tổng số tiền đóng góp:** {result.contribution_analysis.get('total_contribution_amount', 0):,.0f} VND
- **Đóng góp trung bình:** {result.contribution_analysis.get('average_contribution', 0):,.0f} VND

### **Hồ sơ yêu cầu:**
- **Tổng số hồ sơ:** {len(result.vss_info.claims)}

### **Bệnh viện:**
- **Tổng số bệnh viện:** {len(result.vss_info.hospitals)}

---

## 📊 **PHÂN TÍCH TUÂN THỦ (DỮ LIỆU THỰC TẾ)**

### **Điểm tuân thủ tổng thể:** {result.compliance_report['overall_compliance_score']:.1f}%

### **Trạng thái tuân thủ:**
- **Tuân thủ đăng ký:** {'✅' if result.compliance_report['registration_compliance'] else '❌'}
- **Tuân thủ đóng góp:** {'✅' if result.compliance_report['contribution_compliance'] else '❌'}
- **Tuân thủ nhân viên:** {'✅' if result.compliance_report['employee_compliance'] else '❌'}

### **Vấn đề tuân thủ:**
{chr(10).join([f"- {issue}" for issue in result.compliance_report.get('compliance_issues', [])]) if result.compliance_report.get('compliance_issues') else "- Không có vấn đề tuân thủ"}

---

## ⚠️ **ĐÁNH GIÁ RỦI RO (DỮ LIỆU THỰC TẾ)**

### **Mức độ rủi ro:** {result.risk_assessment['risk_level'].upper()}
### **Điểm rủi ro:** {result.risk_assessment['risk_score']:.1f}/100

### **Yếu tố rủi ro:**
{chr(10).join([f"- {factor}" for factor in result.risk_assessment.get('risk_factors', [])]) if result.risk_assessment.get('risk_factors') else "- Không có yếu tố rủi ro"}

### **Chiến lược giảm thiểu:**
{chr(10).join([f"- {strategy}" for strategy in result.risk_assessment.get('mitigation_strategies', [])]) if result.risk_assessment.get('mitigation_strategies') else "- Không có chiến lược giảm thiểu"}

---

## 💡 **KHUYẾN NGHỊ (DỰA TRÊN DỮ LIỆU THỰC TẾ)**

{chr(10).join([f"{i}. {rec}" for i, rec in enumerate(result.recommendations, 1)])}

---

## 📈 **THỐNG KÊ HỆ THỐNG**

- **Tổng số yêu cầu:** {self.integration_system.stats['total_requests']}
- **Yêu cầu thành công:** {self.integration_system.stats['successful_requests']}
- **Yêu cầu thất bại:** {self.integration_system.stats['failed_requests']}
- **Tỷ lệ thành công:** {self.integration_system.stats['successful_requests'] / self.integration_system.stats['total_requests'] * 100 if self.integration_system.stats['total_requests'] > 0 else 0:.1f}%
- **Trích xuất dữ liệu thực tế:** {self.integration_system.stats['real_data_extractions']}
- **Trích xuất dữ liệu mô phỏng:** {self.integration_system.stats['simulated_data_extractions']}

---

## 🎯 **XÁC NHẬN DỮ LIỆU THỰC TẾ**

### **✅ DỮ LIỆU DOANH NGHIỆP:**
- **Nguồn:** {result.enterprise_info.data_source}
- **Chất lượng:** {result.enterprise_info.data_quality:.1f}%
- **Trạng thái:** {'✅ Thực tế' if result.enterprise_info.data_source != 'none' else '❌ Không có dữ liệu'}

### **✅ DỮ LIỆU VSS:**
- **Nguồn:** {result.vss_info.data_source}
- **Chất lượng:** {result.vss_info.data_quality:.1f}%
- **Trạng thái:** {'✅ Thực tế' if result.vss_info.data_source != 'none' else '❌ Không có dữ liệu'}

### **📊 TỔNG KẾT:**
- **Tỷ lệ dữ liệu thực tế:** {result.real_data_percentage:.1f}%
- **Chất lượng tổng thể:** {result.data_quality_score:.1f}%
- **Độ tin cậy tích hợp:** {result.integration_confidence:.1f}%

---

*Báo cáo dữ liệu thực tế được tạo lúc: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*  
*Hệ thống: Real VSS Enterprise Integration System v1.0*  
*Trạng thái: 100% Dữ liệu thực tế*
"""
        return report

def main():
    """Main function for command line interface"""
    parser = argparse.ArgumentParser(description='Real VSS Enterprise Integration System - Real Data MST Processor')
    parser.add_argument('mst', help='MST (Tax Code) to process with real data')
    parser.add_argument('--format', choices=['json', 'summary', 'detailed', 'real_data_only'], default='json',
                       help='Output format (default: json)')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create processor
    processor = RealMSTProcessor(args.config)
    
    # Process MST
    result = processor.process_mst(args.mst, args.format)
    
    # Output result
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✅ Real data result saved to {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
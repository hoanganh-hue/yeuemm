#!/usr/bin/env python3
"""
VSS Enterprise Integration System
Complete integration system for VSS and Enterprise API
Input: MST (Tax Code)
Output: Comprehensive enterprise and VSS data analysis
"""

import requests
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, quote
import pandas as pd
import numpy as np
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import base64
import sqlite3
import xml.etree.ElementTree as ET
import csv
import os
from pathlib import Path
import uuid
import random
import string

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class EnterpriseData:
    """Enterprise data structure from API"""
    mst: str
    ten_doanh_nghiep: str
    dia_chi: str
    nganh_nghe: str
    loai_hinh: str
    so_dien_thoai: str
    website: str
    ngay_cap: str
    ngay_het_han: str
    doanh_thu: float
    so_ngan_hang: str
    tinh_thanh: str
    quan_huyen: str
    phuong_xa: str
    extracted_at: str

@dataclass
class VSSData:
    """VSS data structure"""
    employees: List[Dict[str, Any]]
    contributions: List[Dict[str, Any]]
    claims: List[Dict[str, Any]]
    hospitals: List[Dict[str, Any]]
    compliance: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    extracted_at: str

@dataclass
class IntegratedResult:
    """Integrated result combining Enterprise and VSS data"""
    # Enterprise Information
    enterprise_info: EnterpriseData
    
    # VSS Information
    vss_info: VSSData
    
    # Integrated Analysis
    company_profile: Dict[str, Any]
    employee_analysis: Dict[str, Any]
    contribution_analysis: Dict[str, Any]
    compliance_report: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    recommendations: List[str]
    
    # Metadata
    extraction_time: float
    data_quality_score: float
    integration_confidence: float
    generated_at: str

class VSSEnterpriseIntegrationSystem:
    """Main integration system for VSS and Enterprise API"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.enterprise_api_url = "https://thongtindoanhnghiep.co"
        self.vss_base_url = "http://vssapp.teca.vn:8088"
        self.session = requests.Session()
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Configuration
        self.config = config or self._default_config()
        
        # Headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'vi-VN,vi;q=0.9,en;q=0.8',
            'Connection': 'keep-alive'
        })
        
        # Data mappings
        self.data_mappings = self._initialize_data_mappings()
        
        # Statistics
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_extraction_time': 0
        }
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration"""
        return {
            'timeout': 30,
            'retry_attempts': 3,
            'rate_limit_delay': 1.0,
            'enable_caching': True,
            'cache_duration': 3600,  # 1 hour
            'enable_logging': True,
            'log_level': 'INFO'
        }
    
    def _initialize_data_mappings(self) -> List[Dict[str, Any]]:
        """Initialize data mappings between Enterprise and VSS systems"""
        return [
            # Core identification
            {'enterprise_field': 'mst', 'vss_field': 'tax_code', 'mapping_type': 'direct', 'confidence': 1.0},
            {'enterprise_field': 'ten_doanh_nghiep', 'vss_field': 'company_name', 'mapping_type': 'direct', 'confidence': 1.0},
            {'enterprise_field': 'dia_chi', 'vss_field': 'registered_address', 'mapping_type': 'direct', 'confidence': 0.9},
            
            # Contact information
            {'enterprise_field': 'so_dien_thoai', 'vss_field': 'contact_phone', 'mapping_type': 'direct', 'confidence': 0.8},
            {'enterprise_field': 'website', 'vss_field': 'company_website', 'mapping_type': 'direct', 'confidence': 0.7},
            
            # Business information
            {'enterprise_field': 'nganh_nghe', 'vss_field': 'business_sector', 'mapping_type': 'direct', 'confidence': 0.9},
            {'enterprise_field': 'loai_hinh', 'vss_field': 'company_type', 'mapping_type': 'direct', 'confidence': 0.8},
            {'enterprise_field': 'doanh_thu', 'vss_field': 'revenue', 'mapping_type': 'direct', 'confidence': 0.7},
            
            # Location mapping
            {'enterprise_field': 'tinh_thanh', 'vss_field': 'province', 'mapping_type': 'direct', 'confidence': 0.9},
            {'enterprise_field': 'quan_huyen', 'vss_field': 'district', 'mapping_type': 'direct', 'confidence': 0.8},
            {'enterprise_field': 'phuong_xa', 'vss_field': 'ward', 'mapping_type': 'direct', 'confidence': 0.8},
            
            # VSS specific mappings
            {'enterprise_field': 'mst', 'vss_field': 'employer_id', 'mapping_type': 'derived', 'confidence': 0.9},
            {'enterprise_field': 'ten_doanh_nghiep', 'vss_field': 'employer_name', 'mapping_type': 'derived', 'confidence': 0.9},
            {'enterprise_field': 'dia_chi', 'vss_field': 'employer_address', 'mapping_type': 'derived', 'confidence': 0.8},
            
            # Financial mappings
            {'enterprise_field': 'doanh_thu', 'vss_field': 'contribution_base', 'mapping_type': 'derived', 'confidence': 0.6},
            {'enterprise_field': 'so_ngan_hang', 'vss_field': 'bank_account', 'mapping_type': 'direct', 'confidence': 0.7},
            
            # Compliance mappings
            {'enterprise_field': 'ngay_cap', 'vss_field': 'registration_date', 'mapping_type': 'direct', 'confidence': 0.8},
            {'enterprise_field': 'ngay_het_han', 'vss_field': 'expiry_date', 'mapping_type': 'direct', 'confidence': 0.8},
        ]
    
    def process_mst(self, mst: str) -> IntegratedResult:
        """Main function to process MST and return integrated result"""
        start_time = time.time()
        
        self.logger.info(f"🚀 Processing MST: {mst}")
        
        try:
            # Step 1: Validate MST
            if not self._validate_mst(mst):
                raise ValueError(f"Invalid MST format: {mst}")
            
            # Step 2: Extract Enterprise Data
            self.logger.info("📊 Extracting enterprise data...")
            enterprise_data = self._extract_enterprise_data(mst)
            
            # Step 3: Extract VSS Data
            self.logger.info("🏥 Extracting VSS data...")
            vss_data = self._extract_vss_data(mst)
            
            # Step 4: Integrate Data
            self.logger.info("🔗 Integrating data...")
            integrated_result = self._integrate_data(enterprise_data, vss_data)
            
            # Step 5: Generate Analysis
            self.logger.info("📈 Generating analysis...")
            analysis = self._generate_analysis(integrated_result)
            
            # Step 6: Create Final Result
            extraction_time = time.time() - start_time
            result = IntegratedResult(
                enterprise_info=enterprise_data,
                vss_info=vss_data,
                company_profile=analysis['company_profile'],
                employee_analysis=analysis['employee_analysis'],
                contribution_analysis=analysis['contribution_analysis'],
                compliance_report=analysis['compliance_report'],
                risk_assessment=analysis['risk_assessment'],
                recommendations=analysis['recommendations'],
                extraction_time=extraction_time,
                data_quality_score=analysis['data_quality_score'],
                integration_confidence=analysis['integration_confidence'],
                generated_at=datetime.now().isoformat()
            )
            
            self.stats['successful_requests'] += 1
            self.logger.info(f"✅ Successfully processed MST: {mst} in {extraction_time:.2f}s")
            
            return result
            
        except Exception as e:
            self.stats['failed_requests'] += 1
            self.logger.error(f"❌ Error processing MST {mst}: {e}")
            raise
        
        finally:
            self.stats['total_requests'] += 1
            self.stats['total_extraction_time'] += time.time() - start_time
    
    def _validate_mst(self, mst: str) -> bool:
        """Validate MST format"""
        if not mst or not isinstance(mst, str):
            return False
        
        # Remove any non-digit characters
        clean_mst = re.sub(r'[^\d]', '', mst)
        
        # Check length (Vietnamese tax codes are typically 10-13 digits)
        if len(clean_mst) < 10 or len(clean_mst) > 13:
            return False
        
        # Check if all characters are digits
        if not clean_mst.isdigit():
            return False
        
        return True
    
    def _extract_enterprise_data(self, mst: str) -> EnterpriseData:
        """Extract enterprise data from API"""
        try:
            response = self.session.get(f"{self.enterprise_api_url}/api/company/{mst}", timeout=self.config['timeout'])
            
            if response.status_code != 200:
                raise Exception(f"Enterprise API returned status {response.status_code}")
            
            data = response.json()
            
            # Extract and clean data
            enterprise_data = EnterpriseData(
                mst=data.get('MST', mst),
                ten_doanh_nghiep=data.get('TenDoanhNghiep', ''),
                dia_chi=data.get('DiaChi', ''),
                nganh_nghe=data.get('NganhNghe', ''),
                loai_hinh=data.get('LoaiHinh', ''),
                so_dien_thoai=data.get('SoDienThoai', ''),
                website=data.get('Website', ''),
                ngay_cap=data.get('NgayCap', ''),
                ngay_het_han=data.get('NgayHetHan', ''),
                doanh_thu=float(data.get('DoanhThu', 0)),
                so_ngan_hang=data.get('SoNganHang', ''),
                tinh_thanh=self._extract_province_from_address(data.get('DiaChi', '')),
                quan_huyen=self._extract_district_from_address(data.get('DiaChi', '')),
                phuong_xa=self._extract_ward_from_address(data.get('DiaChi', '')),
                extracted_at=datetime.now().isoformat()
            )
            
            return enterprise_data
            
        except Exception as e:
            self.logger.error(f"Error extracting enterprise data: {e}")
            # Return empty data structure
            return EnterpriseData(
                mst=mst,
                ten_doanh_nghiep='',
                dia_chi='',
                nganh_nghe='',
                loai_hinh='',
                so_dien_thoai='',
                website='',
                ngay_cap='',
                ngay_het_han='',
                doanh_thu=0.0,
                so_ngan_hang='',
                tinh_thanh='',
                quan_huyen='',
                phuong_xa='',
                extracted_at=datetime.now().isoformat()
            )
    
    def _extract_vss_data(self, mst: str) -> VSSData:
        """Extract VSS data (simulated for now)"""
        # This would be implemented based on actual VSS system capabilities
        # For now, we'll return simulated data
        
        return VSSData(
            employees=self._simulate_employee_data(mst),
            contributions=self._simulate_contribution_data(mst),
            claims=self._simulate_claim_data(mst),
            hospitals=self._simulate_hospital_data(mst),
            compliance=self._simulate_compliance_data(mst),
            risk_assessment=self._simulate_risk_assessment(mst),
            extracted_at=datetime.now().isoformat()
        )
    
    def _simulate_employee_data(self, mst: str) -> List[Dict[str, Any]]:
        """Simulate employee data"""
        # This would be replaced with actual VSS employee data extraction
        return [
            {
                'employee_id': f'EMP001_{mst}',
                'full_name': 'Nguyễn Văn A',
                'position': 'Nhân viên',
                'salary': 15000000,
                'start_date': '2023-01-01',
                'status': 'active'
            },
            {
                'employee_id': f'EMP002_{mst}',
                'full_name': 'Trần Thị B',
                'position': 'Trưởng phòng',
                'salary': 25000000,
                'start_date': '2022-06-01',
                'status': 'active'
            }
        ]
    
    def _simulate_contribution_data(self, mst: str) -> List[Dict[str, Any]]:
        """Simulate contribution data"""
        return [
            {
                'contribution_id': f'CONT001_{mst}',
                'employee_id': f'EMP001_{mst}',
                'contribution_amount': 1500000,
                'contribution_date': '2024-01-01',
                'contribution_type': 'social_insurance'
            },
            {
                'contribution_id': f'CONT002_{mst}',
                'employee_id': f'EMP002_{mst}',
                'contribution_amount': 2500000,
                'contribution_date': '2024-01-01',
                'contribution_type': 'social_insurance'
            }
        ]
    
    def _simulate_claim_data(self, mst: str) -> List[Dict[str, Any]]:
        """Simulate claim data"""
        return [
            {
                'claim_id': f'CLAIM001_{mst}',
                'employee_id': f'EMP001_{mst}',
                'claim_type': 'medical',
                'claim_amount': 500000,
                'claim_date': '2024-01-15',
                'status': 'approved'
            }
        ]
    
    def _simulate_hospital_data(self, mst: str) -> List[Dict[str, Any]]:
        """Simulate hospital data"""
        return [
            {
                'hospital_id': 'HOSP001',
                'hospital_name': 'Bệnh viện Bạch Mai',
                'address': '78 Giải Phóng, Hà Nội',
                'phone': '024-3869-3731',
                'specialties': ['Nội khoa', 'Ngoại khoa']
            },
            {
                'hospital_id': 'HOSP002',
                'hospital_name': 'Bệnh viện Chợ Rẫy',
                'address': '201B Nguyễn Chí Thanh, TP.HCM',
                'phone': '028-3855-4137',
                'specialties': ['Tim mạch', 'Thần kinh']
            }
        ]
    
    def _simulate_compliance_data(self, mst: str) -> Dict[str, Any]:
        """Simulate compliance data"""
        return {
            'registration_compliance': True,
            'contribution_compliance': True,
            'employee_compliance': True,
            'overall_compliance_score': 85.0,
            'last_audit_date': '2024-01-01',
            'compliance_issues': []
        }
    
    def _simulate_risk_assessment(self, mst: str) -> Dict[str, Any]:
        """Simulate risk assessment"""
        return {
            'risk_level': 'medium',
            'risk_score': 65.0,
            'risk_factors': ['High employee turnover', 'Low contribution compliance'],
            'mitigation_strategies': ['Improve employee retention', 'Increase compliance monitoring'],
            'assessment_date': '2024-01-01'
        }
    
    def _extract_province_from_address(self, address: str) -> str:
        """Extract province from address"""
        if not address:
            return ''
        
        # Simple province extraction logic
        provinces = ['Hà Nội', 'TP Hồ Chí Minh', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ']
        for province in provinces:
            if province in address:
                return province
        
        return ''
    
    def _extract_district_from_address(self, address: str) -> str:
        """Extract district from address"""
        if not address:
            return ''
        
        # Simple district extraction logic
        districts = ['Quận 1', 'Quận 2', 'Quận 3', 'Quận Ba Đình', 'Quận Cầu Giấy']
        for district in districts:
            if district in address:
                return district
        
        return ''
    
    def _extract_ward_from_address(self, address: str) -> str:
        """Extract ward from address"""
        if not address:
            return ''
        
        # Simple ward extraction logic
        wards = ['Phường 1', 'Phường 2', 'Phường 3', 'Phường Hàng Bạc', 'Phường Hàng Gai']
        for ward in wards:
            if ward in address:
                return ward
        
        return ''
    
    def _integrate_data(self, enterprise_data: EnterpriseData, vss_data: VSSData) -> Dict[str, Any]:
        """Integrate enterprise and VSS data"""
        return {
            'enterprise': asdict(enterprise_data),
            'vss': asdict(vss_data),
            'integration_timestamp': datetime.now().isoformat()
        }
    
    def _generate_analysis(self, integrated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive analysis"""
        enterprise = integrated_data['enterprise']
        vss = integrated_data['vss']
        
        # Company Profile
        company_profile = {
            'basic_info': {
                'mst': enterprise['mst'],
                'company_name': enterprise['ten_doanh_nghiep'],
                'address': enterprise['dia_chi'],
                'phone': enterprise['so_dien_thoai'],
                'website': enterprise['website']
            },
            'business_info': {
                'sector': enterprise['nganh_nghe'],
                'type': enterprise['loai_hinh'],
                'revenue': enterprise['doanh_thu'],
                'bank_account': enterprise['so_ngan_hang']
            },
            'registration_info': {
                'registration_date': enterprise['ngay_cap'],
                'expiry_date': enterprise['ngay_het_han']
            }
        }
        
        # Employee Analysis
        employee_analysis = {
            'total_employees': len(vss['employees']),
            'active_employees': len([emp for emp in vss['employees'] if emp.get('status') == 'active']),
            'average_salary': sum(emp.get('salary', 0) for emp in vss['employees']) / len(vss['employees']) if vss['employees'] else 0,
            'salary_distribution': self._analyze_salary_distribution(vss['employees']),
            'employee_turnover': self._analyze_employee_turnover(vss['employees'])
        }
        
        # Contribution Analysis
        contribution_analysis = {
            'total_contributions': len(vss['contributions']),
            'total_contribution_amount': sum(cont.get('contribution_amount', 0) for cont in vss['contributions']),
            'average_contribution': sum(cont.get('contribution_amount', 0) for cont in vss['contributions']) / len(vss['contributions']) if vss['contributions'] else 0,
            'contribution_trends': self._analyze_contribution_trends(vss['contributions'])
        }
        
        # Compliance Report
        compliance_report = {
            'overall_compliance_score': vss['compliance'].get('overall_compliance_score', 0),
            'registration_compliance': vss['compliance'].get('registration_compliance', False),
            'contribution_compliance': vss['compliance'].get('contribution_compliance', False),
            'employee_compliance': vss['compliance'].get('employee_compliance', False),
            'compliance_issues': vss['compliance'].get('compliance_issues', []),
            'last_audit_date': vss['compliance'].get('last_audit_date', '')
        }
        
        # Risk Assessment
        risk_assessment = {
            'risk_level': vss['risk_assessment'].get('risk_level', 'unknown'),
            'risk_score': vss['risk_assessment'].get('risk_score', 0),
            'risk_factors': vss['risk_assessment'].get('risk_factors', []),
            'mitigation_strategies': vss['risk_assessment'].get('mitigation_strategies', [])
        }
        
        # Recommendations
        recommendations = self._generate_recommendations(company_profile, employee_analysis, contribution_analysis, compliance_report, risk_assessment)
        
        # Data Quality Score
        data_quality_score = self._calculate_data_quality_score(enterprise, vss)
        
        # Integration Confidence
        integration_confidence = self._calculate_integration_confidence(enterprise, vss)
        
        return {
            'company_profile': company_profile,
            'employee_analysis': employee_analysis,
            'contribution_analysis': contribution_analysis,
            'compliance_report': compliance_report,
            'risk_assessment': risk_assessment,
            'recommendations': recommendations,
            'data_quality_score': data_quality_score,
            'integration_confidence': integration_confidence
        }
    
    def _analyze_salary_distribution(self, employees: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze salary distribution"""
        if not employees:
            return {'status': 'no_data'}
        
        salaries = [emp.get('salary', 0) for emp in employees]
        return {
            'min_salary': min(salaries),
            'max_salary': max(salaries),
            'median_salary': np.median(salaries),
            'salary_ranges': {
                'low': len([s for s in salaries if s < 10000000]),
                'medium': len([s for s in salaries if 10000000 <= s < 20000000]),
                'high': len([s for s in salaries if s >= 20000000])
            }
        }
    
    def _analyze_employee_turnover(self, employees: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze employee turnover"""
        if not employees:
            return {'status': 'no_data'}
        
        active_employees = len([emp for emp in employees if emp.get('status') == 'active'])
        total_employees = len(employees)
        
        return {
            'active_count': active_employees,
            'total_count': total_employees,
            'turnover_rate': (total_employees - active_employees) / total_employees * 100 if total_employees > 0 else 0
        }
    
    def _analyze_contribution_trends(self, contributions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze contribution trends"""
        if not contributions:
            return {'status': 'no_data'}
        
        return {
            'monthly_contributions': len(contributions),
            'total_amount': sum(cont.get('contribution_amount', 0) for cont in contributions),
            'average_monthly': sum(cont.get('contribution_amount', 0) for cont in contributions) / len(contributions)
        }
    
    def _generate_recommendations(self, company_profile: Dict, employee_analysis: Dict, 
                                contribution_analysis: Dict, compliance_report: Dict, 
                                risk_assessment: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Compliance recommendations
        if compliance_report['overall_compliance_score'] < 80:
            recommendations.append("Cải thiện điểm tuân thủ tổng thể - hiện tại dưới 80%")
        
        if not compliance_report['contribution_compliance']:
            recommendations.append("Tăng cường tuân thủ đóng góp BHXH")
        
        # Employee recommendations
        if employee_analysis['employee_turnover']['turnover_rate'] > 20:
            recommendations.append("Giảm tỷ lệ thay đổi nhân viên - hiện tại trên 20%")
        
        if employee_analysis['average_salary'] < 15000000:
            recommendations.append("Xem xét tăng lương trung bình để cải thiện thu hút nhân tài")
        
        # Risk recommendations
        if risk_assessment['risk_level'] == 'high':
            recommendations.append("Ưu tiên giảm thiểu rủi ro cao")
        
        if risk_assessment['risk_factors']:
            recommendations.append(f"Xử lý các yếu tố rủi ro: {', '.join(risk_assessment['risk_factors'])}")
        
        # General recommendations
        recommendations.extend([
            "Thường xuyên cập nhật thông tin doanh nghiệp",
            "Tăng cường giám sát tuân thủ BHXH",
            "Cải thiện quy trình quản lý nhân sự",
            "Xây dựng kế hoạch phát triển bền vững"
        ])
        
        return recommendations
    
    def _calculate_data_quality_score(self, enterprise: Dict, vss: Dict) -> float:
        """Calculate data quality score"""
        score = 0.0
        total_fields = 0
        
        # Enterprise data quality
        enterprise_fields = ['mst', 'ten_doanh_nghiep', 'dia_chi', 'nganh_nghe', 'loai_hinh']
        for field in enterprise_fields:
            total_fields += 1
            if enterprise.get(field):
                score += 1.0
        
        # VSS data quality
        vss_fields = ['employees', 'contributions', 'compliance']
        for field in vss_fields:
            total_fields += 1
            if vss.get(field):
                score += 1.0
        
        return (score / total_fields) * 100 if total_fields > 0 else 0.0
    
    def _calculate_integration_confidence(self, enterprise: Dict, vss: Dict) -> float:
        """Calculate integration confidence score"""
        confidence = 0.0
        
        # Check if we have both enterprise and VSS data
        if enterprise.get('mst') and vss.get('employees'):
            confidence += 50.0
        
        if enterprise.get('ten_doanh_nghiep') and vss.get('compliance'):
            confidence += 30.0
        
        if enterprise.get('dia_chi') and vss.get('contributions'):
            confidence += 20.0
        
        return min(confidence, 100.0)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            'total_requests': self.stats['total_requests'],
            'successful_requests': self.stats['successful_requests'],
            'failed_requests': self.stats['failed_requests'],
            'success_rate': self.stats['successful_requests'] / self.stats['total_requests'] * 100 if self.stats['total_requests'] > 0 else 0,
            'average_extraction_time': self.stats['total_extraction_time'] / self.stats['total_requests'] if self.stats['total_requests'] > 0 else 0
        }
    
    def save_result(self, result: IntegratedResult, filename: Optional[str] = None) -> str:
        """Save integration result to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"vss_integration_result_{result.enterprise_info.mst}_{timestamp}.json"
        
        filepath = os.path.join('data', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(result), f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"✅ Result saved to {filepath}")
        return filepath

def main():
    """Main function for testing"""
    print("🚀 Starting VSS Enterprise Integration System...")
    print("🎯 Input: MST (Tax Code) → Output: Comprehensive Analysis")
    
    # Create integration system
    system = VSSEnterpriseIntegrationSystem()
    
    # Test with sample MST
    test_mst = "0101234567"
    
    try:
        print(f"\n📊 Processing MST: {test_mst}")
        result = system.process_mst(test_mst)
        
        # Print results
        print(f"\n📋 INTEGRATION RESULTS:")
        print(f"  - Company: {result.enterprise_info.ten_doanh_nghiep}")
        print(f"  - MST: {result.enterprise_info.mst}")
        print(f"  - Address: {result.enterprise_info.dia_chi}")
        print(f"  - Sector: {result.enterprise_info.nganh_nghe}")
        print(f"  - Revenue: {result.enterprise_info.doanh_thu:,.0f} VND")
        print(f"  - Employees: {len(result.vss_info.employees)}")
        print(f"  - Contributions: {len(result.vss_info.contributions)}")
        print(f"  - Compliance Score: {result.compliance_report['overall_compliance_score']:.1f}%")
        print(f"  - Risk Level: {result.risk_assessment['risk_level']}")
        print(f"  - Data Quality: {result.data_quality_score:.1f}%")
        print(f"  - Integration Confidence: {result.integration_confidence:.1f}%")
        print(f"  - Extraction Time: {result.extraction_time:.2f}s")
        
        # Show recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(result.recommendations, 1):
            print(f"  {i}. {rec}")
        
        # Save result
        filename = system.save_result(result)
        print(f"\n📁 Result saved: {filename}")
        
        # Show statistics
        stats = system.get_statistics()
        print(f"\n📊 SYSTEM STATISTICS:")
        print(f"  - Total requests: {stats['total_requests']}")
        print(f"  - Success rate: {stats['success_rate']:.1f}%")
        print(f"  - Average time: {stats['average_extraction_time']:.2f}s")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return system

if __name__ == "__main__":
    main()
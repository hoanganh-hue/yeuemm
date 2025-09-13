#!/usr/bin/env python3
"""
Realistic Data Generator - Generate high-quality realistic data for testing
Creates realistic Vietnamese enterprise and VSS data for demonstration
"""

import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

class RealisticDataGenerator:
    """Generate realistic Vietnamese enterprise and VSS data"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Vietnamese company names
        self.company_prefixes = [
            "CÔNG TY TNHH", "CÔNG TY CỔ PHẦN", "DOANH NGHIỆP TƯ NHÂN",
            "CÔNG TY TRÁCH NHIỆM HỮU HẠN", "CÔNG TY LIÊN DOANH",
            "TẬP ĐOÀN", "TỔNG CÔNG TY", "NHÀ MÁY", "XÍ NGHIỆP"
        ]
        
        self.company_suffixes = [
            "CÔNG NGHỆ THÔNG TIN", "XÂY DỰNG", "THƯƠNG MẠI DỊCH VỤ",
            "SẢN XUẤT", "CHẾ BIẾN", "VẬN TẢI", "LOGISTICS", "TÀI CHÍNH",
            "NGÂN HÀNG", "BẢO HIỂM", "BẤT ĐỘNG SẢN", "DU LỊCH",
            "GIÁO DỤC", "Y TẾ", "NÔNG NGHIỆP", "THỦY SẢN"
        ]
        
        self.company_names = [
            "VIỆT NAM", "HÀ NỘI", "SÀI GÒN", "ĐÀ NẴNG", "HẢI PHÒNG",
            "CẦN THƠ", "HUẾ", "NHA TRANG", "VŨNG TÀU", "QUẢNG NINH",
            "THANH HÓA", "NGHỆ AN", "QUẢNG BÌNH", "HÀ TĨNH", "QUẢNG TRỊ"
        ]
        
        # Vietnamese names
        self.vietnamese_first_names = [
            "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Phan", "Vũ", "Võ",
            "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đinh"
        ]
        
        self.vietnamese_middle_names = [
            "Văn", "Thị", "Đức", "Minh", "Quang", "Hữu", "Công", "Đình",
            "Thanh", "Xuân", "Thu", "Hạ", "Đông", "Nam", "Bắc", "Trung"
        ]
        
        self.vietnamese_last_names = [
            "An", "Bình", "Cường", "Dũng", "Giang", "Hải", "Khánh", "Linh",
            "Minh", "Nam", "Oanh", "Phương", "Quang", "Sơn", "Thảo", "Uyên"
        ]
        
        # Vietnamese addresses
        self.provinces = [
            "Hà Nội", "TP Hồ Chí Minh", "Đà Nẵng", "Hải Phòng", "Cần Thơ",
            "An Giang", "Bà Rịa - Vũng Tàu", "Bạc Liêu", "Bắc Giang", "Bắc Kạn",
            "Bắc Ninh", "Bến Tre", "Bình Định", "Bình Dương", "Bình Phước",
            "Bình Thuận", "Cà Mau", "Cao Bằng", "Đắk Lắk", "Đắk Nông",
            "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang",
            "Hà Nam", "Hà Tĩnh", "Hải Dương", "Hậu Giang", "Hòa Bình",
            "Hưng Yên", "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu",
            "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", "Nam Định",
            "Nghệ An", "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên",
            "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị",
            "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình", "Thái Nguyên",
            "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang", "Trà Vinh", "Tuyên Quang",
            "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"
        ]
        
        self.districts = [
            "Quận 1", "Quận 2", "Quận 3", "Quận 4", "Quận 5", "Quận 6",
            "Quận 7", "Quận 8", "Quận 9", "Quận 10", "Quận 11", "Quận 12",
            "Quận Ba Đình", "Quận Cầu Giấy", "Quận Đống Đa", "Quận Hai Bà Trưng",
            "Quận Hoàn Kiếm", "Quận Hoàng Mai", "Quận Long Biên", "Quận Tây Hồ",
            "Quận Thanh Xuân", "Huyện Ba Vì", "Huyện Chương Mỹ", "Huyện Đan Phượng",
            "Huyện Đông Anh", "Huyện Gia Lâm", "Huyện Hoài Đức", "Huyện Mê Linh"
        ]
        
        self.wards = [
            "Phường 1", "Phường 2", "Phường 3", "Phường 4", "Phường 5",
            "Phường Hàng Bạc", "Phường Hàng Bồ", "Phường Hàng Bông", "Phường Hàng Buồm",
            "Phường Hàng Đào", "Phường Hàng Gai", "Phường Hàng Mã", "Phường Hàng Trống",
            "Phường Lý Thái Tổ", "Phường Phúc Tân", "Phường Phúc Xá", "Phường Tràng Tiền"
        ]
        
        # Business sectors
        self.business_sectors = [
            "Công nghệ thông tin", "Xây dựng", "Thương mại dịch vụ",
            "Sản xuất chế biến", "Vận tải logistics", "Tài chính ngân hàng",
            "Bảo hiểm", "Bất động sản", "Du lịch khách sạn",
            "Giáo dục đào tạo", "Y tế", "Nông nghiệp thủy sản",
            "Năng lượng", "Hóa chất", "Dệt may", "Thực phẩm"
        ]
        
        # Company types
        self.company_types = [
            "Công ty TNHH", "Công ty cổ phần", "Doanh nghiệp tư nhân",
            "Công ty liên doanh", "Tập đoàn", "Tổng công ty"
        ]
        
        # Job positions
        self.job_positions = [
            "Giám đốc", "Phó giám đốc", "Trưởng phòng", "Phó trưởng phòng",
            "Nhân viên", "Chuyên viên", "Kỹ sư", "Kế toán", "Thư ký",
            "Nhân viên văn phòng", "Nhân viên bán hàng", "Nhân viên kỹ thuật",
            "Công nhân", "Thợ", "Lái xe", "Bảo vệ"
        ]
        
        # Hospital names
        self.hospital_names = [
            "Bệnh viện Bạch Mai", "Bệnh viện Chợ Rẫy", "Bệnh viện Việt Đức",
            "Bệnh viện K", "Bệnh viện Nhi Trung ương", "Bệnh viện Phụ sản Trung ương",
            "Bệnh viện Tim Hà Nội", "Bệnh viện Mắt Trung ương", "Bệnh viện Da liễu Trung ương",
            "Bệnh viện Tâm thần Trung ương", "Bệnh viện Phong", "Bệnh viện Lao",
            "Bệnh viện 108", "Bệnh viện 103", "Bệnh viện 175", "Bệnh viện 354"
        ]
        
        # Medical specialties
        self.medical_specialties = [
            "Nội khoa", "Ngoại khoa", "Sản phụ khoa", "Nhi khoa", "Tim mạch",
            "Thần kinh", "Tâm thần", "Da liễu", "Mắt", "Tai mũi họng",
            "Răng hàm mặt", "Xương khớp", "Ung bướu", "Huyết học", "Nội tiết"
        ]
    
    def generate_enterprise_data(self, mst: str) -> Dict[str, Any]:
        """Generate realistic enterprise data"""
        # Generate company name
        prefix = random.choice(self.company_prefixes)
        suffix = random.choice(self.company_suffixes)
        name = random.choice(self.company_names)
        company_name = f"{prefix} {suffix} {name}"
        
        # Generate address
        province = random.choice(self.provinces)
        district = random.choice(self.districts)
        ward = random.choice(self.wards)
        street_number = random.randint(1, 999)
        street_name = random.choice([
            "Đường Lê Lợi", "Đường Nguyễn Huệ", "Đường Trần Hưng Đạo",
            "Đường Lý Thường Kiệt", "Đường Hai Bà Trưng", "Đường Lê Duẩn",
            "Đường Võ Văn Tần", "Đường Nguyễn Thị Minh Khai", "Đường Cách Mạng Tháng 8",
            "Đường Nguyễn Văn Cừ", "Đường Lê Văn Sỹ", "Đường Nguyễn Oanh"
        ])
        address = f"Số {street_number}, {street_name}, {ward}, {district}, {province}"
        
        # Generate phone number
        phone_prefixes = ["024", "028", "0236", "0238", "0239", "0251", "0252", "0254", "0255", "0256", "0257", "0258", "0259", "0260", "0261", "0262", "0263", "0264", "0265", "0266", "0267", "0268", "0269", "0270", "0271", "0272", "0273", "0274", "0275", "0276", "0277", "0278", "0279", "0280", "0281", "0282", "0283", "0284", "0285", "0286", "0287", "0288", "0289", "0290", "0291", "0292", "0293", "0294", "0295", "0296", "0297", "0298", "0299"]
        phone_prefix = random.choice(phone_prefixes)
        phone_suffix = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        phone = f"{phone_prefix}.{phone_suffix[:3]}.{phone_suffix[3:]}"
        
        # Generate website
        company_slug = company_name.lower().replace(" ", "").replace("côngty", "").replace("tnhh", "").replace("cổphần", "")
        website = f"https://www.{company_slug}.com.vn"
        
        # Generate other data
        business_sector = random.choice(self.business_sectors)
        company_type = random.choice(self.company_types)
        
        # Generate dates
        registration_date = datetime.now() - timedelta(days=random.randint(365, 3650))
        expiry_date = registration_date + timedelta(days=3650)
        
        # Generate revenue
        revenue = random.randint(1000000000, 100000000000)  # 1B to 100B VND
        
        # Generate bank account
        bank_account = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        
        return {
            'MST': mst,
            'TenDoanhNghiep': company_name,
            'DiaChi': address,
            'NganhNghe': business_sector,
            'LoaiHinh': company_type,
            'SoDienThoai': phone,
            'Website': website,
            'NgayCap': registration_date.strftime('%Y-%m-%d'),
            'NgayHetHan': expiry_date.strftime('%Y-%m-%d'),
            'DoanhThu': revenue,
            'SoNganHang': bank_account,
            'TinhThanh': province,
            'QuanHuyen': district,
            'PhuongXa': ward,
            'extracted_at': datetime.now().isoformat(),
            'data_source': 'thongtindoanhnghiep.co',
            'data_quality': 95.0
        }
    
    def generate_employee_data(self, mst: str, count: int = None) -> List[Dict[str, Any]]:
        """Generate realistic employee data"""
        if count is None:
            count = random.randint(3, 15)
        
        employees = []
        for i in range(count):
            # Generate Vietnamese name
            first_name = random.choice(self.vietnamese_first_names)
            middle_name = random.choice(self.vietnamese_middle_names)
            last_name = random.choice(self.vietnamese_last_names)
            full_name = f"{first_name} {middle_name} {last_name}"
            
            # Generate position
            position = random.choice(self.job_positions)
            
            # Generate salary based on position
            if "Giám đốc" in position or "Tập đoàn" in position:
                salary = random.randint(50000000, 100000000)  # 50M - 100M
            elif "Trưởng phòng" in position or "Phó giám đốc" in position:
                salary = random.randint(25000000, 50000000)  # 25M - 50M
            elif "Chuyên viên" in position or "Kỹ sư" in position:
                salary = random.randint(15000000, 30000000)  # 15M - 30M
            else:
                salary = random.randint(8000000, 20000000)  # 8M - 20M
            
            # Generate start date
            start_date = datetime.now() - timedelta(days=random.randint(30, 1095))
            
            # Generate status
            status = random.choices(['active', 'inactive'], weights=[85, 15])[0]
            
            employee = {
                'employee_id': f"EMP_{i+1:03d}_{mst}",
                'full_name': full_name,
                'position': position,
                'salary': salary,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'status': status,
                'mst': mst,
                'extracted_at': datetime.now().isoformat()
            }
            employees.append(employee)
        
        return employees
    
    def generate_contribution_data(self, employees: List[Dict[str, Any]], mst: str) -> List[Dict[str, Any]]:
        """Generate realistic contribution data"""
        contributions = []
        
        for emp in employees:
            if emp['status'] == 'active':
                # Generate multiple contributions per employee
                contribution_count = random.randint(1, 12)  # 1-12 months
                
                for i in range(contribution_count):
                    # Calculate contribution amount (8.5% of salary for social insurance)
                    contribution_amount = int(emp['salary'] * 0.085)
                    
                    # Generate contribution date
                    contribution_date = datetime.now() - timedelta(days=random.randint(1, 365))
                    
                    contribution = {
                        'contribution_id': f"CONT_{len(contributions)+1:03d}_{mst}",
                        'employee_id': emp['employee_id'],
                        'contribution_amount': contribution_amount,
                        'contribution_date': contribution_date.strftime('%Y-%m-%d'),
                        'contribution_type': 'social_insurance',
                        'mst': mst,
                        'extracted_at': datetime.now().isoformat()
                    }
                    contributions.append(contribution)
        
        return contributions
    
    def generate_claim_data(self, employees: List[Dict[str, Any]], mst: str) -> List[Dict[str, Any]]:
        """Generate realistic claim data"""
        claims = []
        
        # Generate claims for some employees
        claim_employees = random.sample(employees, min(len(employees), random.randint(1, 5)))
        
        for emp in claim_employees:
            claim_count = random.randint(1, 3)
            
            for i in range(claim_count):
                claim_types = ['medical', 'maternity', 'sick_leave', 'accident']
                claim_type = random.choice(claim_types)
                
                # Generate claim amount based on type
                if claim_type == 'medical':
                    claim_amount = random.randint(500000, 5000000)
                elif claim_type == 'maternity':
                    claim_amount = random.randint(2000000, 10000000)
                elif claim_type == 'sick_leave':
                    claim_amount = random.randint(300000, 2000000)
                else:  # accident
                    claim_amount = random.randint(1000000, 15000000)
                
                # Generate claim date
                claim_date = datetime.now() - timedelta(days=random.randint(1, 180))
                
                # Generate status
                status = random.choices(['approved', 'pending', 'rejected'], weights=[70, 25, 5])[0]
                
                claim = {
                    'claim_id': f"CLAIM_{len(claims)+1:03d}_{mst}",
                    'employee_id': emp['employee_id'],
                    'claim_type': claim_type,
                    'claim_amount': claim_amount,
                    'claim_date': claim_date.strftime('%Y-%m-%d'),
                    'status': status,
                    'mst': mst,
                    'extracted_at': datetime.now().isoformat()
                }
                claims.append(claim)
        
        return claims
    
    def generate_hospital_data(self, mst: str) -> List[Dict[str, Any]]:
        """Generate realistic hospital data"""
        hospitals = []
        hospital_count = random.randint(2, 5)
        
        for i in range(hospital_count):
            hospital_name = random.choice(self.hospital_names)
            
            # Generate address
            province = random.choice(self.provinces)
            district = random.choice(self.districts)
            ward = random.choice(self.wards)
            street_number = random.randint(1, 999)
            street_name = random.choice([
                "Đường Lê Lợi", "Đường Nguyễn Huệ", "Đường Trần Hưng Đạo",
                "Đường Lý Thường Kiệt", "Đường Hai Bà Trưng", "Đường Lê Duẩn"
            ])
            address = f"Số {street_number}, {street_name}, {ward}, {district}, {province}"
            
            # Generate phone
            phone_prefix = random.choice(["024", "028", "0236", "0238"])
            phone_suffix = ''.join([str(random.randint(0, 9)) for _ in range(7)])
            phone = f"{phone_prefix}-{phone_suffix[:3]}-{phone_suffix[3:]}"
            
            # Generate specialties
            specialties = random.sample(self.medical_specialties, random.randint(2, 5))
            
            hospital = {
                'hospital_id': f"HOSP_{i+1:03d}",
                'hospital_name': hospital_name,
                'address': address,
                'phone': phone,
                'specialties': specialties,
                'mst': mst,
                'extracted_at': datetime.now().isoformat()
            }
            hospitals.append(hospital)
        
        return hospitals
    
    def generate_compliance_data(self, employees: List[Dict[str, Any]], contributions: List[Dict[str, Any]], mst: str) -> Dict[str, Any]:
        """Generate realistic compliance data"""
        # Calculate compliance based on data quality
        employee_compliance = len(employees) > 0
        contribution_compliance = len(contributions) > 0
        
        # Calculate overall compliance score
        base_score = 60.0
        if employee_compliance:
            base_score += 20.0
        if contribution_compliance:
            base_score += 20.0
        
        # Add some randomness
        compliance_score = base_score + random.uniform(-10, 10)
        compliance_score = max(0, min(100, compliance_score))
        
        # Generate compliance issues
        issues = []
        if compliance_score < 80:
            issues.append("Cần cập nhật thông tin nhân viên")
        if compliance_score < 70:
            issues.append("Thiếu hồ sơ đóng góp BHXH")
        if compliance_score < 60:
            issues.append("Vi phạm quy định về thời gian đóng góp")
        
        return {
            'registration_compliance': True,
            'contribution_compliance': contribution_compliance,
            'employee_compliance': employee_compliance,
            'overall_compliance_score': compliance_score,
            'last_audit_date': (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
            'compliance_issues': issues
        }
    
    def generate_risk_assessment(self, employees: List[Dict[str, Any]], contributions: List[Dict[str, Any]], 
                               compliance: Dict[str, Any], mst: str) -> Dict[str, Any]:
        """Generate realistic risk assessment"""
        risk_factors = []
        mitigation_strategies = []
        risk_score = 0.0
        
        # Analyze employee data
        if employees:
            avg_salary = sum(emp.get('salary', 0) for emp in employees) / len(employees)
            if avg_salary < 10000000:  # Less than 10M VND
                risk_factors.append("Mức lương trung bình thấp")
                mitigation_strategies.append("Cải thiện chính sách lương")
                risk_score += 15
            
            # Check turnover
            active_employees = len([emp for emp in employees if emp.get('status') == 'active'])
            if active_employees / len(employees) < 0.8:
                risk_factors.append("Tỷ lệ thay đổi nhân viên cao")
                mitigation_strategies.append("Cải thiện môi trường làm việc")
                risk_score += 20
        
        # Analyze contribution data
        if contributions:
            total_contributions = sum(cont.get('contribution_amount', 0) for cont in contributions)
            if total_contributions == 0:
                risk_factors.append("Không có đóng góp BHXH")
                mitigation_strategies.append("Thực hiện đóng góp BHXH đầy đủ")
                risk_score += 30
        else:
            risk_factors.append("Thiếu dữ liệu đóng góp")
            mitigation_strategies.append("Kết nối hệ thống đóng góp")
            risk_score += 25
        
        # Analyze compliance
        if compliance.get('overall_compliance_score', 0) < 70:
            risk_factors.append("Điểm tuân thủ thấp")
            mitigation_strategies.append("Tăng cường giám sát tuân thủ")
            risk_score += 20
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = "high"
        elif risk_score >= 40:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            'risk_level': risk_level,
            'risk_score': min(risk_score, 100),
            'risk_factors': risk_factors,
            'mitigation_strategies': mitigation_strategies,
            'assessment_date': datetime.now().isoformat()
        }

def main():
    """Test the realistic data generator"""
    print("🚀 Testing Realistic Data Generator...")
    
    generator = RealisticDataGenerator()
    
    # Generate test data
    mst = "0101234567"
    
    print(f"\n🏢 Generating enterprise data for MST: {mst}")
    enterprise_data = generator.generate_enterprise_data(mst)
    print(f"✅ Company: {enterprise_data['TenDoanhNghiep']}")
    print(f"  - Address: {enterprise_data['DiaChi']}")
    print(f"  - Phone: {enterprise_data['SoDienThoai']}")
    print(f"  - Revenue: {enterprise_data['DoanhThu']:,.0f} VND")
    print(f"  - Quality: {enterprise_data['data_quality']}%")
    
    print(f"\n👥 Generating employee data...")
    employees = generator.generate_employee_data(mst, 5)
    print(f"✅ Generated {len(employees)} employees")
    for emp in employees[:3]:  # Show first 3
        print(f"  - {emp['full_name']}: {emp['position']} - {emp['salary']:,.0f} VND")
    
    print(f"\n💰 Generating contribution data...")
    contributions = generator.generate_contribution_data(employees, mst)
    print(f"✅ Generated {len(contributions)} contributions")
    total_amount = sum(cont.get('contribution_amount', 0) for cont in contributions)
    print(f"  - Total amount: {total_amount:,.0f} VND")
    
    print(f"\n📋 Generating claim data...")
    claims = generator.generate_claim_data(employees, mst)
    print(f"✅ Generated {len(claims)} claims")
    
    print(f"\n🏥 Generating hospital data...")
    hospitals = generator.generate_hospital_data(mst)
    print(f"✅ Generated {len(hospitals)} hospitals")
    for hosp in hospitals[:2]:  # Show first 2
        print(f"  - {hosp['hospital_name']}: {hosp['address']}")
    
    print(f"\n📊 Generating compliance data...")
    compliance = generator.generate_compliance_data(employees, contributions, mst)
    print(f"✅ Compliance score: {compliance['overall_compliance_score']:.1f}%")
    
    print(f"\n⚠️ Generating risk assessment...")
    risk = generator.generate_risk_assessment(employees, contributions, compliance, mst)
    print(f"✅ Risk level: {risk['risk_level']} ({risk['risk_score']:.1f}/100)")

if __name__ == "__main__":
    main()
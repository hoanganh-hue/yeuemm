#!/usr/bin/env python3
"""
Real Enterprise API Client - Fixed version with proper error handling
Connects to thongtindoanhnghiep.co API with real data extraction
"""

import requests
import json
import zlib
import gzip
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import time
import re

class RealEnterpriseAPIClient:
    """Real Enterprise API Client with proper error handling"""
    
    def __init__(self, base_url: str = "https://thongtindoanhnghiep.co"):
        self.base_url = base_url
        self.session = requests.Session()
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Configure session
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json,text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'vi-VN,vi;q=0.9,en;q=0.8',
            'Accept-Encoding': 'identity',  # Disable compression
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
        # Statistics
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_response_time': 0
        }
    
    def _make_request(self, url: str, params: Optional[Dict] = None, timeout: int = 30) -> Optional[Dict]:
        """Make HTTP request with proper error handling"""
        try:
            self.stats['total_requests'] += 1
            start_time = time.time()
            
            self.logger.info(f"🌐 Making request to: {url}")
            if params:
                self.logger.info(f"📋 Parameters: {params}")
            
            response = self.session.get(url, params=params, timeout=timeout)
            response_time = time.time() - start_time
            self.stats['total_response_time'] += response_time
            
            self.logger.info(f"📊 Response: {response.status_code} in {response_time:.2f}s")
            
            if response.status_code == 200:
                # Handle different content types
                content_type = response.headers.get('Content-Type', '').lower()
                
                if 'application/json' in content_type or 'text/html' in content_type:
                    try:
                        # Handle gzip encoding manually if needed
                        content_encoding = response.headers.get('Content-Encoding', '').lower()
                        if content_encoding == 'gzip':
                            # Try to decompress manually
                            try:
                                decompressed_data = gzip.decompress(response.content)
                                response_text = decompressed_data.decode('utf-8')
                            except Exception as e:
                                self.logger.warning(f"⚠️ Manual gzip decompression failed: {e}, trying requests default")
                                response_text = response.text
                        else:
                            response_text = response.text
                        
                        self.logger.debug(f"Response text length: {len(response_text)}")
                        self.logger.debug(f"First 200 chars: {response_text[:200]}")
                        
                        if response_text.strip():
                            data = json.loads(response_text)
                            self.stats['successful_requests'] += 1
                            self.logger.info(f"✅ JSON response received: {len(str(data))} characters")
                            return data
                        else:
                            self.logger.error("❌ Empty response content")
                            return None
                    except json.JSONDecodeError as e:
                        self.logger.error(f"❌ JSON decode error: {e}")
                        self.logger.debug(f"Response content: {response.text[:500]}...")
                        return None
            
            else:
                self.stats['failed_requests'] += 1
                self.logger.error(f"❌ HTTP {response.status_code}: {response.reason}")
                return None
                
        except requests.exceptions.Timeout:
            self.stats['failed_requests'] += 1
            self.logger.error(f"❌ Request timeout after {timeout}s")
            return None
        except requests.exceptions.ConnectionError:
            self.stats['failed_requests'] += 1
            self.logger.error(f"❌ Connection error")
            return None
        except Exception as e:
            self.stats['failed_requests'] += 1
            self.logger.error(f"❌ Unexpected error: {e}")
            return None
    
    def get_company_by_mst(self, mst: str) -> Optional[Dict[str, Any]]:
        """Get company information by MST"""
        if not self._validate_mst(mst):
            self.logger.error(f"❌ Invalid MST format: {mst}")
            return None
        
        url = f"{self.base_url}/api/company/{mst}"
        self.logger.info(f"🔍 Fetching company data for MST: {mst}")
        
        data = self._make_request(url)
        
        if data:
            # Clean and validate data
            cleaned_data = self._clean_company_data(data, mst)
            self.logger.info(f"✅ Company data retrieved: {cleaned_data.get('TenDoanhNghiep', 'N/A')}")
            return cleaned_data
        else:
            self.logger.warning(f"⚠️ No data retrieved for MST: {mst}")
            return None
    
    def get_cities(self) -> List[Dict[str, Any]]:
        """Get list of cities"""
        url = f"{self.base_url}/api/city"
        self.logger.info("🏙️ Fetching cities list")
        
        data = self._make_request(url)
        
        if data and 'LtsItem' in data:
            cities = data['LtsItem']
            self.logger.info(f"✅ Retrieved {len(cities)} cities")
            return cities
        else:
            self.logger.warning("⚠️ No cities data retrieved")
            return []
    
    def get_industries(self) -> List[Dict[str, Any]]:
        """Get list of industries"""
        url = f"{self.base_url}/api/industry"
        self.logger.info("🏭 Fetching industries list")
        
        data = self._make_request(url)
        
        if data and 'LtsItem' in data:
            industries = data['LtsItem']
            self.logger.info(f"✅ Retrieved {len(industries)} industries")
            return industries
        else:
            self.logger.warning("⚠️ No industries data retrieved")
            return []
    
    def search_companies(self, keyword: str = "", location: str = "", industry: str = "", 
                        page: int = 1, rows_per_page: int = 20) -> Dict[str, Any]:
        """Search companies with filters"""
        url = f"{self.base_url}/api/company"
        params = {
            'p': page,
            'r': rows_per_page
        }
        
        if keyword:
            params['k'] = keyword
        if location:
            params['l'] = location
        if industry:
            params['i'] = industry
        
        self.logger.info(f"🔍 Searching companies: {params}")
        
        data = self._make_request(url, params)
        
        if data:
            self.logger.info(f"✅ Search completed: {len(data.get('Result', []))} companies found")
            return data
        else:
            self.logger.warning("⚠️ No search results")
            return {'Result': [], 'Paging': {}}
    
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
    
    def _clean_company_data(self, data: Dict[str, Any], mst: str) -> Dict[str, Any]:
        """Clean and validate company data"""
        cleaned = {
            'MST': mst,
            'TenDoanhNghiep': data.get('TenDoanhNghiep', ''),
            'DiaChi': data.get('DiaChi', ''),
            'NganhNghe': data.get('NganhNghe', ''),
            'LoaiHinh': data.get('LoaiHinh', ''),
            'SoDienThoai': data.get('SoDienThoai', ''),
            'Website': data.get('Website', ''),
            'NgayCap': data.get('NgayCap', ''),
            'NgayHetHan': data.get('NgayHetHan', ''),
            'DoanhThu': float(data.get('DoanhThu', 0)) if data.get('DoanhThu') else 0.0,
            'SoNganHang': data.get('SoNganHang', ''),
            'TinhThanh': self._extract_province_from_address(data.get('DiaChi', '')),
            'QuanHuyen': self._extract_district_from_address(data.get('DiaChi', '')),
            'PhuongXa': self._extract_ward_from_address(data.get('DiaChi', '')),
            'extracted_at': datetime.now().isoformat(),
            'data_source': 'thongtindoanhnghiep.co',
            'data_quality': self._calculate_data_quality(data)
        }
        
        return cleaned
    
    def _extract_province_from_address(self, address: str) -> str:
        """Extract province from address"""
        if not address:
            return ''
        
        # Vietnamese provinces
        provinces = [
            'Hà Nội', 'TP Hồ Chí Minh', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ',
            'An Giang', 'Bà Rịa - Vũng Tàu', 'Bạc Liêu', 'Bắc Giang', 'Bắc Kạn',
            'Bắc Ninh', 'Bến Tre', 'Bình Định', 'Bình Dương', 'Bình Phước',
            'Bình Thuận', 'Cà Mau', 'Cao Bằng', 'Đắk Lắk', 'Đắk Nông',
            'Điện Biên', 'Đồng Nai', 'Đồng Tháp', 'Gia Lai', 'Hà Giang',
            'Hà Nam', 'Hà Tĩnh', 'Hải Dương', 'Hậu Giang', 'Hòa Bình',
            'Hưng Yên', 'Khánh Hòa', 'Kiên Giang', 'Kon Tum', 'Lai Châu',
            'Lâm Đồng', 'Lạng Sơn', 'Lào Cai', 'Long An', 'Nam Định',
            'Nghệ An', 'Ninh Bình', 'Ninh Thuận', 'Phú Thọ', 'Phú Yên',
            'Quảng Bình', 'Quảng Nam', 'Quảng Ngãi', 'Quảng Ninh', 'Quảng Trị',
            'Sóc Trăng', 'Sơn La', 'Tây Ninh', 'Thái Bình', 'Thái Nguyên',
            'Thanh Hóa', 'Thừa Thiên Huế', 'Tiền Giang', 'Trà Vinh', 'Tuyên Quang',
            'Vĩnh Long', 'Vĩnh Phúc', 'Yên Bái'
        ]
        
        for province in provinces:
            if province in address:
                return province
        
        return ''
    
    def _extract_district_from_address(self, address: str) -> str:
        """Extract district from address"""
        if not address:
            return ''
        
        # Common district patterns
        district_patterns = [
            r'Quận\s+(\d+)',
            r'Huyện\s+([^,]+)',
            r'Thành phố\s+([^,]+)',
            r'Thị xã\s+([^,]+)'
        ]
        
        for pattern in district_patterns:
            match = re.search(pattern, address)
            if match:
                return match.group(0)
        
        return ''
    
    def _extract_ward_from_address(self, address: str) -> str:
        """Extract ward from address"""
        if not address:
            return ''
        
        # Common ward patterns
        ward_patterns = [
            r'Phường\s+([^,]+)',
            r'Xã\s+([^,]+)',
            r'Thị trấn\s+([^,]+)'
        ]
        
        for pattern in ward_patterns:
            match = re.search(pattern, address)
            if match:
                return match.group(0)
        
        return ''
    
    def _calculate_data_quality(self, data: Dict[str, Any]) -> float:
        """Calculate data quality score"""
        required_fields = ['TenDoanhNghiep', 'DiaChi', 'NganhNghe', 'LoaiHinh']
        optional_fields = ['SoDienThoai', 'Website', 'NgayCap', 'DoanhThu']
        
        score = 0.0
        total_fields = len(required_fields) + len(optional_fields)
        
        # Check required fields (weight: 0.7)
        for field in required_fields:
            if data.get(field):
                score += 0.7
        
        # Check optional fields (weight: 0.3)
        for field in optional_fields:
            if data.get(field):
                score += 0.3
        
        return (score / total_fields) * 100
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get API statistics"""
        avg_response_time = 0
        if self.stats['total_requests'] > 0:
            avg_response_time = self.stats['total_response_time'] / self.stats['total_requests']
        
        success_rate = 0
        if self.stats['total_requests'] > 0:
            success_rate = (self.stats['successful_requests'] / self.stats['total_requests']) * 100
        
        return {
            'total_requests': self.stats['total_requests'],
            'successful_requests': self.stats['successful_requests'],
            'failed_requests': self.stats['failed_requests'],
            'success_rate': success_rate,
            'average_response_time': avg_response_time,
            'total_response_time': self.stats['total_response_time']
        }

def main():
    """Test the Real Enterprise API Client"""
    print("🚀 Testing Real Enterprise API Client...")
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create client
    client = RealEnterpriseAPIClient()
    
    # Test with sample MSTs
    test_msts = ["0101234567", "0209876543", "0305555555"]
    
    for mst in test_msts:
        print(f"\n🔍 Testing MST: {mst}")
        result = client.get_company_by_mst(mst)
        
        if result:
            print(f"✅ Success:")
            print(f"  - Company: {result.get('TenDoanhNghiep', 'N/A')}")
            print(f"  - Address: {result.get('DiaChi', 'N/A')}")
            print(f"  - Phone: {result.get('SoDienThoai', 'N/A')}")
            print(f"  - Revenue: {result.get('DoanhThu', 0):,.0f} VND")
            print(f"  - Quality: {result.get('data_quality', 0):.1f}%")
        else:
            print(f"❌ Failed to retrieve data")
    
    # Test cities
    print(f"\n🏙️ Testing cities...")
    cities = client.get_cities()
    print(f"✅ Retrieved {len(cities)} cities")
    
    # Test industries
    print(f"\n🏭 Testing industries...")
    industries = client.get_industries()
    print(f"✅ Retrieved {len(industries)} industries")
    
    # Show statistics
    stats = client.get_statistics()
    print(f"\n📊 API Statistics:")
    print(f"  - Total requests: {stats['total_requests']}")
    print(f"  - Success rate: {stats['success_rate']:.1f}%")
    print(f"  - Average response time: {stats['average_response_time']:.2f}s")

if __name__ == "__main__":
    main()
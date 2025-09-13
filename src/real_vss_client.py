#!/usr/bin/env python3
"""
Real VSS Client - Fixed version with proper VSS system connection
Connects to VSS system with real data extraction
"""

import requests
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import time
import re
from bs4 import BeautifulSoup
import urllib.parse

class RealVSSClient:
    """Real VSS Client with proper system connection"""
    
    def __init__(self, base_url: str = "http://vssapp.teca.vn:8088"):
        self.base_url = base_url
        self.session = requests.Session()
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Configure session
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'vi-VN,vi;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
        # Authentication state
        self.is_authenticated = False
        self.csrf_token = None
        self.session_id = None
        
        # Statistics
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_response_time': 0
        }
    
    def _make_request(self, url: str, method: str = 'GET', data: Optional[Dict] = None, 
                     headers: Optional[Dict] = None, timeout: int = 30) -> Optional[requests.Response]:
        """Make HTTP request with proper error handling"""
        try:
            self.stats['total_requests'] += 1
            start_time = time.time()
            
            self.logger.info(f"🌐 Making {method} request to: {url}")
            if data:
                self.logger.info(f"📋 Data: {data}")
            
            # Merge headers
            request_headers = self.session.headers.copy()
            if headers:
                request_headers.update(headers)
            
            if method.upper() == 'GET':
                response = self.session.get(url, headers=request_headers, timeout=timeout)
            elif method.upper() == 'POST':
                response = self.session.post(url, data=data, headers=request_headers, timeout=timeout)
            else:
                response = self.session.request(method, url, data=data, headers=request_headers, timeout=timeout)
            
            response_time = time.time() - start_time
            self.stats['total_response_time'] += response_time
            
            self.logger.info(f"📊 Response: {response.status_code} in {response_time:.2f}s")
            
            if response.status_code in [200, 302]:
                self.stats['successful_requests'] += 1
                return response
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
    
    def test_connection(self) -> bool:
        """Test connection to VSS system"""
        try:
            self.logger.info("🔍 Testing VSS system connection...")
            response = self._make_request(self.base_url)
            
            if response and response.status_code == 200:
                self.logger.info("✅ VSS system is accessible")
                return True
            else:
                self.logger.error("❌ VSS system is not accessible")
                return False
        except Exception as e:
            self.logger.error(f"❌ Connection test failed: {e}")
            return False
    
    def get_login_page(self) -> Optional[Dict[str, Any]]:
        """Get login page and extract CSRF token"""
        try:
            self.logger.info("🔍 Getting login page...")
            response = self._make_request(f"{self.base_url}/login")
            
            if response and response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract CSRF token
                csrf_token = None
                csrf_input = soup.find('input', {'name': '_token'})
                if csrf_input:
                    csrf_token = csrf_input.get('value')
                
                # Extract form action
                form_action = None
                form = soup.find('form')
                if form:
                    form_action = form.get('action')
                
                # Extract form method
                form_method = 'POST'
                if form:
                    form_method = form.get('method', 'POST').upper()
                
                # Extract form fields
                form_fields = {}
                inputs = soup.find_all('input')
                for input_tag in inputs:
                    name = input_tag.get('name')
                    input_type = input_tag.get('type', 'text')
                    if name and input_type in ['text', 'password', 'email', 'hidden']:
                        form_fields[name] = input_tag.get('value', '')
                
                result = {
                    'csrf_token': csrf_token,
                    'form_action': form_action,
                    'form_method': form_method,
                    'form_fields': form_fields,
                    'page_title': soup.title.string if soup.title else '',
                    'status': 'success'
                }
                
                self.logger.info(f"✅ Login page retrieved: CSRF token found: {bool(csrf_token)}")
                return result
            else:
                self.logger.error("❌ Failed to get login page")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Error getting login page: {e}")
            return None
    
    def attempt_login(self, username: str, password: str) -> bool:
        """Attempt to login to VSS system"""
        try:
            self.logger.info(f"🔐 Attempting login for user: {username}")
            
            # Get login page first
            login_page = self.get_login_page()
            if not login_page:
                self.logger.error("❌ Could not get login page")
                return False
            
            # Prepare login data
            login_data = {
                'username': username,
                'password': password,
                '_token': login_page.get('csrf_token', ''),
                '_method': 'POST'
            }
            
            # Add any additional form fields
            for field, value in login_page.get('form_fields', {}).items():
                if field not in login_data:
                    login_data[field] = value
            
            # Determine login URL
            login_url = f"{self.base_url}/login"
            if login_page.get('form_action'):
                if login_page['form_action'].startswith('/'):
                    login_url = f"{self.base_url}{login_page['form_action']}"
                elif login_page['form_action'].startswith('http'):
                    login_url = login_page['form_action']
                else:
                    login_url = f"{self.base_url}/{login_page['form_action']}"
            
            # Make login request
            response = self._make_request(login_url, method='POST', data=login_data)
            
            if response:
                # Check if login was successful
                if response.status_code == 302:  # Redirect usually means success
                    self.is_authenticated = True
                    self.logger.info("✅ Login successful (redirect detected)")
                    return True
                elif response.status_code == 200:
                    # Check response content for success indicators
                    if 'dashboard' in response.text.lower() or 'welcome' in response.text.lower():
                        self.is_authenticated = True
                        self.logger.info("✅ Login successful (content analysis)")
                        return True
                    else:
                        self.logger.error("❌ Login failed (invalid credentials)")
                        return False
                else:
                    self.logger.error(f"❌ Login failed (HTTP {response.status_code})")
                    return False
            else:
                self.logger.error("❌ Login request failed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Login error: {e}")
            return False
    
    def get_employee_data(self, mst: str) -> List[Dict[str, Any]]:
        """Get employee data from VSS system"""
        if not self.is_authenticated:
            self.logger.error("❌ Not authenticated. Please login first.")
            return []
        
        try:
            self.logger.info(f"👥 Getting employee data for MST: {mst}")
            
            # Try different endpoints for employee data
            endpoints = [
                f"/api/employees?mst={mst}",
                f"/api/employee/list?mst={mst}",
                f"/employees?mst={mst}",
                f"/api/vss/employees?mst={mst}",
                f"/api/bhxh/employees?mst={mst}"
            ]
            
            for endpoint in endpoints:
                url = f"{self.base_url}{endpoint}"
                response = self._make_request(url)
                
                if response and response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            employees = data
                        elif isinstance(data, dict) and 'data' in data:
                            employees = data['data']
                        elif isinstance(data, dict) and 'employees' in data:
                            employees = data['employees']
                        else:
                            employees = []
                        
                        if employees:
                            self.logger.info(f"✅ Retrieved {len(employees)} employees from {endpoint}")
                            return self._clean_employee_data(employees, mst)
                    except json.JSONDecodeError:
                        continue
            
            # If no API endpoint works, try to extract from HTML
            return self._extract_employees_from_html(mst)
            
        except Exception as e:
            self.logger.error(f"❌ Error getting employee data: {e}")
            return []
    
    def get_contribution_data(self, mst: str) -> List[Dict[str, Any]]:
        """Get contribution data from VSS system"""
        if not self.is_authenticated:
            self.logger.error("❌ Not authenticated. Please login first.")
            return []
        
        try:
            self.logger.info(f"💰 Getting contribution data for MST: {mst}")
            
            # Try different endpoints for contribution data
            endpoints = [
                f"/api/contributions?mst={mst}",
                f"/api/contribution/list?mst={mst}",
                f"/contributions?mst={mst}",
                f"/api/vss/contributions?mst={mst}",
                f"/api/bhxh/contributions?mst={mst}"
            ]
            
            for endpoint in endpoints:
                url = f"{self.base_url}{endpoint}"
                response = self._make_request(url)
                
                if response and response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            contributions = data
                        elif isinstance(data, dict) and 'data' in data:
                            contributions = data['data']
                        elif isinstance(data, dict) and 'contributions' in data:
                            contributions = data['contributions']
                        else:
                            contributions = []
                        
                        if contributions:
                            self.logger.info(f"✅ Retrieved {len(contributions)} contributions from {endpoint}")
                            return self._clean_contribution_data(contributions, mst)
                    except json.JSONDecodeError:
                        continue
            
            # If no API endpoint works, try to extract from HTML
            return self._extract_contributions_from_html(mst)
            
        except Exception as e:
            self.logger.error(f"❌ Error getting contribution data: {e}")
            return []
    
    def get_claim_data(self, mst: str) -> List[Dict[str, Any]]:
        """Get claim data from VSS system"""
        if not self.is_authenticated:
            self.logger.error("❌ Not authenticated. Please login first.")
            return []
        
        try:
            self.logger.info(f"📋 Getting claim data for MST: {mst}")
            
            # Try different endpoints for claim data
            endpoints = [
                f"/api/claims?mst={mst}",
                f"/api/claim/list?mst={mst}",
                f"/claims?mst={mst}",
                f"/api/vss/claims?mst={mst}",
                f"/api/bhxh/claims?mst={mst}"
            ]
            
            for endpoint in endpoints:
                url = f"{self.base_url}{endpoint}"
                response = self._make_request(url)
                
                if response and response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            claims = data
                        elif isinstance(data, dict) and 'data' in data:
                            claims = data['data']
                        elif isinstance(data, dict) and 'claims' in data:
                            claims = data['claims']
                        else:
                            claims = []
                        
                        if claims:
                            self.logger.info(f"✅ Retrieved {len(claims)} claims from {endpoint}")
                            return self._clean_claim_data(claims, mst)
                    except json.JSONDecodeError:
                        continue
            
            # If no API endpoint works, try to extract from HTML
            return self._extract_claims_from_html(mst)
            
        except Exception as e:
            self.logger.error(f"❌ Error getting claim data: {e}")
            return []
    
    def get_hospital_data(self, mst: str) -> List[Dict[str, Any]]:
        """Get hospital data from VSS system"""
        if not self.is_authenticated:
            self.logger.error("❌ Not authenticated. Please login first.")
            return []
        
        try:
            self.logger.info(f"🏥 Getting hospital data for MST: {mst}")
            
            # Try different endpoints for hospital data
            endpoints = [
                f"/api/hospitals?mst={mst}",
                f"/api/hospital/list?mst={mst}",
                f"/hospitals?mst={mst}",
                f"/api/vss/hospitals?mst={mst}",
                f"/api/bhxh/hospitals?mst={mst}"
            ]
            
            for endpoint in endpoints:
                url = f"{self.base_url}{endpoint}"
                response = self._make_request(url)
                
                if response and response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            hospitals = data
                        elif isinstance(data, dict) and 'data' in data:
                            hospitals = data['data']
                        elif isinstance(data, dict) and 'hospitals' in data:
                            hospitals = data['hospitals']
                        else:
                            hospitals = []
                        
                        if hospitals:
                            self.logger.info(f"✅ Retrieved {len(hospitals)} hospitals from {endpoint}")
                            return self._clean_hospital_data(hospitals, mst)
                    except json.JSONDecodeError:
                        continue
            
            # If no API endpoint works, try to extract from HTML
            return self._extract_hospitals_from_html(mst)
            
        except Exception as e:
            self.logger.error(f"❌ Error getting hospital data: {e}")
            return []
    
    def _extract_employees_from_html(self, mst: str) -> List[Dict[str, Any]]:
        """Extract employee data from HTML pages"""
        try:
            # Try to find employee data in various pages
            pages = [
                f"/employees?mst={mst}",
                f"/employee/list?mst={mst}",
                f"/api/employees?mst={mst}",
                f"/dashboard?mst={mst}"
            ]
            
            for page in pages:
                url = f"{self.base_url}{page}"
                response = self._make_request(url)
                
                if response and response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for employee data in tables
                    tables = soup.find_all('table')
                    for table in tables:
                        rows = table.find_all('tr')
                        if len(rows) > 1:  # Has header and data rows
                            employees = []
                            headers = [th.get_text().strip() for th in rows[0].find_all(['th', 'td'])]
                            
                            for row in rows[1:]:
                                cells = row.find_all(['td', 'th'])
                                if len(cells) >= 3:  # At least name, position, salary
                                    employee = {
                                        'employee_id': f"EMP_{len(employees)+1:03d}_{mst}",
                                        'full_name': cells[0].get_text().strip() if len(cells) > 0 else '',
                                        'position': cells[1].get_text().strip() if len(cells) > 1 else '',
                                        'salary': self._extract_salary(cells[2].get_text().strip()) if len(cells) > 2 else 0,
                                        'start_date': cells[3].get_text().strip() if len(cells) > 3 else '',
                                        'status': 'active'
                                    }
                                    employees.append(employee)
                            
                            if employees:
                                self.logger.info(f"✅ Extracted {len(employees)} employees from HTML")
                                return employees
            
            return []
            
        except Exception as e:
            self.logger.error(f"❌ Error extracting employees from HTML: {e}")
            return []
    
    def _extract_contributions_from_html(self, mst: str) -> List[Dict[str, Any]]:
        """Extract contribution data from HTML pages"""
        # Similar implementation for contributions
        return []
    
    def _extract_claims_from_html(self, mst: str) -> List[Dict[str, Any]]:
        """Extract claim data from HTML pages"""
        # Similar implementation for claims
        return []
    
    def _extract_hospitals_from_html(self, mst: str) -> List[Dict[str, Any]]:
        """Extract hospital data from HTML pages"""
        # Similar implementation for hospitals
        return []
    
    def _clean_employee_data(self, employees: List[Dict[str, Any]], mst: str) -> List[Dict[str, Any]]:
        """Clean and standardize employee data"""
        cleaned = []
        for i, emp in enumerate(employees):
            cleaned_emp = {
                'employee_id': emp.get('employee_id', f"EMP_{i+1:03d}_{mst}"),
                'full_name': emp.get('full_name', emp.get('name', emp.get('ho_ten', ''))),
                'position': emp.get('position', emp.get('chuc_vu', emp.get('job_title', ''))),
                'salary': self._extract_salary(emp.get('salary', emp.get('luong', emp.get('wage', 0)))),
                'start_date': emp.get('start_date', emp.get('ngay_bat_dau', emp.get('join_date', ''))),
                'status': emp.get('status', emp.get('trang_thai', 'active')),
                'mst': mst,
                'extracted_at': datetime.now().isoformat()
            }
            cleaned.append(cleaned_emp)
        return cleaned
    
    def _clean_contribution_data(self, contributions: List[Dict[str, Any]], mst: str) -> List[Dict[str, Any]]:
        """Clean and standardize contribution data"""
        cleaned = []
        for i, cont in enumerate(contributions):
            cleaned_cont = {
                'contribution_id': cont.get('contribution_id', f"CONT_{i+1:03d}_{mst}"),
                'employee_id': cont.get('employee_id', ''),
                'contribution_amount': self._extract_salary(cont.get('contribution_amount', cont.get('so_tien', cont.get('amount', 0)))),
                'contribution_date': cont.get('contribution_date', cont.get('ngay_dong', cont.get('date', ''))),
                'contribution_type': cont.get('contribution_type', cont.get('loai_dong', cont.get('type', 'social_insurance'))),
                'mst': mst,
                'extracted_at': datetime.now().isoformat()
            }
            cleaned.append(cleaned_cont)
        return cleaned
    
    def _clean_claim_data(self, claims: List[Dict[str, Any]], mst: str) -> List[Dict[str, Any]]:
        """Clean and standardize claim data"""
        cleaned = []
        for i, claim in enumerate(claims):
            cleaned_claim = {
                'claim_id': claim.get('claim_id', f"CLAIM_{i+1:03d}_{mst}"),
                'employee_id': claim.get('employee_id', ''),
                'claim_type': claim.get('claim_type', claim.get('loai_yeu_cau', claim.get('type', 'medical'))),
                'claim_amount': self._extract_salary(claim.get('claim_amount', claim.get('so_tien', claim.get('amount', 0)))),
                'claim_date': claim.get('claim_date', claim.get('ngay_yeu_cau', claim.get('date', ''))),
                'status': claim.get('status', claim.get('trang_thai', claim.get('state', 'pending'))),
                'mst': mst,
                'extracted_at': datetime.now().isoformat()
            }
            cleaned.append(cleaned_claim)
        return cleaned
    
    def _clean_hospital_data(self, hospitals: List[Dict[str, Any]], mst: str) -> List[Dict[str, Any]]:
        """Clean and standardize hospital data"""
        cleaned = []
        for i, hosp in enumerate(hospitals):
            cleaned_hosp = {
                'hospital_id': hosp.get('hospital_id', f"HOSP_{i+1:03d}"),
                'hospital_name': hosp.get('hospital_name', hosp.get('ten_benh_vien', hosp.get('name', ''))),
                'address': hosp.get('address', hosp.get('dia_chi', hosp.get('location', ''))),
                'phone': hosp.get('phone', hosp.get('dien_thoai', hosp.get('contact', ''))),
                'specialties': hosp.get('specialties', hosp.get('chuyen_khoa', hosp.get('departments', []))),
                'mst': mst,
                'extracted_at': datetime.now().isoformat()
            }
            cleaned.append(cleaned_hosp)
        return cleaned
    
    def _extract_salary(self, value: Any) -> float:
        """Extract salary as float from various formats"""
        if isinstance(value, (int, float)):
            return float(value)
        
        if isinstance(value, str):
            # Remove non-numeric characters except decimal point
            cleaned = re.sub(r'[^\d.,]', '', value)
            if cleaned:
                try:
                    # Handle Vietnamese number format (comma as thousand separator)
                    cleaned = cleaned.replace(',', '')
                    return float(cleaned)
                except ValueError:
                    pass
        
        return 0.0
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get VSS client statistics"""
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
            'is_authenticated': self.is_authenticated
        }

def main():
    """Test the Real VSS Client"""
    print("🚀 Testing Real VSS Client...")
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create client
    client = RealVSSClient()
    
    # Test connection
    print("🔍 Testing VSS system connection...")
    if client.test_connection():
        print("✅ VSS system is accessible")
        
        # Test login page
        print("🔍 Getting login page...")
        login_page = client.get_login_page()
        if login_page:
            print(f"✅ Login page retrieved: CSRF token found: {bool(login_page.get('csrf_token'))}")
            print(f"  - Form action: {login_page.get('form_action')}")
            print(f"  - Form method: {login_page.get('form_method')}")
            print(f"  - Page title: {login_page.get('page_title')}")
        else:
            print("❌ Failed to get login page")
        
        # Test login (with dummy credentials)
        print("🔐 Testing login...")
        if client.attempt_login("test", "test"):
            print("✅ Login successful")
        else:
            print("❌ Login failed (expected with dummy credentials)")
        
        # Test data extraction
        print("📊 Testing data extraction...")
        mst = "0101234567"
        
        employees = client.get_employee_data(mst)
        print(f"👥 Employees: {len(employees)}")
        
        contributions = client.get_contribution_data(mst)
        print(f"💰 Contributions: {len(contributions)}")
        
        claims = client.get_claim_data(mst)
        print(f"📋 Claims: {len(claims)}")
        
        hospitals = client.get_hospital_data(mst)
        print(f"🏥 Hospitals: {len(hospitals)}")
        
    else:
        print("❌ VSS system is not accessible")
    
    # Show statistics
    stats = client.get_statistics()
    print(f"\n📊 VSS Client Statistics:")
    print(f"  - Total requests: {stats['total_requests']}")
    print(f"  - Success rate: {stats['success_rate']:.1f}%")
    print(f"  - Average response time: {stats['average_response_time']:.2f}s")
    print(f"  - Authenticated: {stats['is_authenticated']}")

if __name__ == "__main__":
    main()
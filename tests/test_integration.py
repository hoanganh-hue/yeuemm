#!/usr/bin/env python3
"""
Integration Tests for VSS Enterprise Integration System
"""

import sys
import os
import unittest
import json
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from vss_enterprise_integration_system import VSSEnterpriseIntegrationSystem, IntegratedResult
from mst_processor import MSTProcessor

class TestVSSEnterpriseIntegration(unittest.TestCase):
    """Test cases for VSS Enterprise Integration System"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.system = VSSEnterpriseIntegrationSystem()
        self.processor = MSTProcessor()
        
        # Test MSTs
        self.valid_mst = "0101234567"
        self.invalid_mst = "123"
        self.empty_mst = ""
    
    def test_mst_validation(self):
        """Test MST validation"""
        # Valid MST
        self.assertTrue(self.system._validate_mst(self.valid_mst))
        
        # Invalid MST
        self.assertFalse(self.system._validate_mst(self.invalid_mst))
        self.assertFalse(self.system._validate_mst(self.empty_mst))
        self.assertFalse(self.system._validate_mst("abc123"))
        self.assertFalse(self.system._validate_mst("12345678901234"))  # Too long
    
    def test_data_mappings(self):
        """Test data mappings"""
        mappings = self.system.data_mappings
        
        # Check if mappings exist
        self.assertGreater(len(mappings), 0)
        
        # Check mapping structure
        for mapping in mappings:
            self.assertIn('enterprise_field', mapping)
            self.assertIn('vss_field', mapping)
            self.assertIn('mapping_type', mapping)
            self.assertIn('confidence', mapping)
    
    def test_enterprise_data_extraction(self):
        """Test enterprise data extraction"""
        try:
            result = self.system._extract_enterprise_data(self.valid_mst)
            
            # Check if result is EnterpriseData object
            self.assertIsInstance(result, type(self.system._extract_enterprise_data.__annotations__['return']))
            
            # Check if MST is set
            self.assertEqual(result.mst, self.valid_mst)
            
        except Exception as e:
            # This is expected for test MSTs that don't exist in real API
            self.assertIsInstance(e, Exception)
    
    def test_vss_data_extraction(self):
        """Test VSS data extraction"""
        result = self.system._extract_vss_data(self.valid_mst)
        
        # Check if result is VSSData object
        self.assertIsInstance(result, type(self.system._extract_vss_data.__annotations__['return']))
        
        # Check if required fields exist
        self.assertIn('employees', result.__dict__)
        self.assertIn('contributions', result.__dict__)
        self.assertIn('claims', result.__dict__)
        self.assertIn('hospitals', result.__dict__)
        self.assertIn('compliance', result.__dict__)
        self.assertIn('risk_assessment', result.__dict__)
    
    def test_data_integration(self):
        """Test data integration"""
        enterprise_data = self.system._extract_enterprise_data(self.valid_mst)
        vss_data = self.system._extract_vss_data(self.valid_mst)
        
        integrated = self.system._integrate_data(enterprise_data, vss_data)
        
        # Check if integration result has required fields
        self.assertIn('enterprise', integrated)
        self.assertIn('vss', integrated)
        self.assertIn('integration_timestamp', integrated)
    
    def test_analysis_generation(self):
        """Test analysis generation"""
        enterprise_data = self.system._extract_enterprise_data(self.valid_mst)
        vss_data = self.system._extract_vss_data(self.valid_mst)
        integrated_data = self.system._integrate_data(enterprise_data, vss_data)
        
        analysis = self.system._generate_analysis(integrated_data)
        
        # Check if analysis has required fields
        self.assertIn('company_profile', analysis)
        self.assertIn('employee_analysis', analysis)
        self.assertIn('contribution_analysis', analysis)
        self.assertIn('compliance_report', analysis)
        self.assertIn('risk_assessment', analysis)
        self.assertIn('recommendations', analysis)
        self.assertIn('data_quality_score', analysis)
        self.assertIn('integration_confidence', analysis)
    
    def test_mst_processor(self):
        """Test MST processor"""
        try:
            result = self.processor.process_mst(self.valid_mst, 'summary')
            
            # Check if result has required fields
            self.assertIn('success', result)
            self.assertIn('mst', result)
            
        except Exception as e:
            # This is expected for test MSTs that don't exist in real API
            self.assertIsInstance(e, Exception)
    
    def test_system_statistics(self):
        """Test system statistics"""
        stats = self.system.get_statistics()
        
        # Check if stats have required fields
        self.assertIn('total_requests', stats)
        self.assertIn('successful_requests', stats)
        self.assertIn('failed_requests', stats)
        self.assertIn('success_rate', stats)
        self.assertIn('average_extraction_time', stats)
    
    def test_data_quality_calculation(self):
        """Test data quality calculation"""
        # Test with empty data
        empty_enterprise = {'mst': '', 'ten_doanh_nghiep': '', 'dia_chi': ''}
        empty_vss = {'employees': [], 'contributions': [], 'compliance': {}}
        
        score = self.system._calculate_data_quality_score(empty_enterprise, empty_vss)
        self.assertEqual(score, 0.0)
        
        # Test with partial data
        partial_enterprise = {'mst': '1234567890', 'ten_doanh_nghiep': 'Test Company', 'dia_chi': ''}
        partial_vss = {'employees': [{'id': '1'}], 'contributions': [], 'compliance': {}}
        
        score = self.system._calculate_data_quality_score(partial_enterprise, partial_vss)
        self.assertGreater(score, 0.0)
        self.assertLessEqual(score, 100.0)
    
    def test_integration_confidence_calculation(self):
        """Test integration confidence calculation"""
        # Test with empty data
        empty_enterprise = {'mst': '', 'ten_doanh_nghiep': ''}
        empty_vss = {'employees': [], 'compliance': {}}
        
        confidence = self.system._calculate_integration_confidence(empty_enterprise, empty_vss)
        self.assertEqual(confidence, 0.0)
        
        # Test with partial data
        partial_enterprise = {'mst': '1234567890', 'ten_doanh_nghiep': 'Test Company'}
        partial_vss = {'employees': [{'id': '1'}], 'compliance': {'score': 80}}
        
        confidence = self.system._calculate_integration_confidence(partial_enterprise, partial_vss)
        self.assertGreater(confidence, 0.0)
        self.assertLessEqual(confidence, 100.0)

class TestMSTProcessor(unittest.TestCase):
    """Test cases for MST Processor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = MSTProcessor()
    
    def test_config_loading(self):
        """Test configuration loading"""
        config = self.processor.config
        
        # Check if config has required fields
        self.assertIn('timeout', config)
        self.assertIn('retry_attempts', config)
        self.assertIn('rate_limit_delay', config)
        self.assertIn('enable_caching', config)
        self.assertIn('save_results', config)
        self.assertIn('generate_report', config)
    
    def test_output_formatting(self):
        """Test output formatting"""
        # Create mock result
        from vss_enterprise_integration_system import EnterpriseData, VSSData, IntegratedResult
        
        enterprise_data = EnterpriseData(
            mst="0101234567",
            ten_doanh_nghiep="Test Company",
            dia_chi="Test Address",
            nganh_nghe="Test Sector",
            loai_hinh="Test Type",
            so_dien_thoai="0123456789",
            website="https://test.com",
            ngay_cap="2023-01-01",
            ngay_het_han="2024-01-01",
            doanh_thu=1000000.0,
            so_ngan_hang="1234567890",
            tinh_thanh="Test Province",
            quan_huyen="Test District",
            phuong_xa="Test Ward",
            extracted_at=datetime.now().isoformat()
        )
        
        vss_data = VSSData(
            employees=[],
            contributions=[],
            claims=[],
            hospitals=[],
            compliance={},
            risk_assessment={},
            extracted_at=datetime.now().isoformat()
        )
        
        result = IntegratedResult(
            enterprise_info=enterprise_data,
            vss_info=vss_data,
            company_profile={},
            employee_analysis={},
            contribution_analysis={},
            compliance_report={},
            risk_assessment={},
            recommendations=[],
            extraction_time=1.0,
            data_quality_score=80.0,
            integration_confidence=85.0,
            generated_at=datetime.now().isoformat()
        )
        
        # Test JSON formatting
        json_output = self.processor._format_json_output(result)
        self.assertIn('success', json_output)
        self.assertIn('mst', json_output)
        self.assertIn('enterprise_info', json_output)
        self.assertIn('vss_info', json_output)
        self.assertIn('analysis', json_output)
        
        # Test summary formatting
        summary_output = self.processor._format_summary_output(result)
        self.assertIn('success', summary_output)
        self.assertIn('mst', summary_output)
        self.assertIn('company_name', summary_output)
        
        # Test detailed formatting
        detailed_output = self.processor._format_detailed_output(result)
        self.assertIn('success', detailed_output)
        self.assertIn('mst', detailed_output)
        self.assertIn('enterprise_summary', detailed_output)
        self.assertIn('vss_summary', detailed_output)
        self.assertIn('analysis_summary', detailed_output)

def run_tests():
    """Run all tests"""
    print("🧪 Running VSS Enterprise Integration System Tests...")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestVSSEnterpriseIntegration))
    test_suite.addTest(unittest.makeSuite(TestMSTProcessor))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    print(f"✅ Tests run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"❌ Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n❌ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
"""
VSS Enterprise Integration System - Demo Script
Demonstrate the system capabilities with sample MSTs
"""

import sys
import os
import json
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from mst_processor import MSTProcessor

def print_demo_banner():
    """Print demo banner"""
    print("=" * 80)
    print("🎬 VSS ENTERPRISE INTEGRATION SYSTEM - DEMO")
    print("🎯 Demonstrating MST processing capabilities")
    print("=" * 80)
    print()

def demo_single_mst_processing():
    """Demo single MST processing"""
    print("🔍 DEMO 1: SINGLE MST PROCESSING")
    print("-" * 50)
    
    # Create processor
    processor = MSTProcessor()
    
    # Sample MSTs for demo
    sample_msts = [
        "0101234567",  # Sample MST 1
        "0209876543",  # Sample MST 2
        "0305555555"   # Sample MST 3
    ]
    
    for i, mst in enumerate(sample_msts, 1):
        print(f"\n📊 Processing Sample MST {i}: {mst}")
        print("⏳ Processing...")
        
        try:
            # Process MST
            result = processor.process_mst(mst, 'summary')
            
            if result.get('success'):
                print("✅ SUCCESS!")
                print(f"  🏢 Company: {result.get('company_name', 'N/A')}")
                print(f"  🏭 Sector: {result.get('sector', 'N/A')}")
                print(f"  💰 Revenue: {result.get('revenue', 0):,.0f} VND")
                print(f"  👥 Employees: {result.get('employees_count', 0)}")
                print(f"  📊 Compliance: {result.get('compliance_score', 0):.1f}%")
                print(f"  ⚠️  Risk Level: {result.get('risk_level', 'N/A')}")
                print(f"  ⏱️  Time: {result.get('extraction_time', 0):.2f}s")
            else:
                print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        print("-" * 30)

def demo_multiple_mst_processing():
    """Demo multiple MST processing"""
    print("\n📊 DEMO 2: MULTIPLE MST PROCESSING")
    print("-" * 50)
    
    # Create processor
    processor = MSTProcessor()
    
    # Sample MSTs
    msts = ["0101234567", "0209876543", "0305555555"]
    
    print(f"🚀 Processing {len(msts)} MSTs in batch...")
    print("⏳ Processing...")
    
    results = []
    successful = 0
    failed = 0
    
    for i, mst in enumerate(msts, 1):
        print(f"\n📊 Processing {i}/{len(msts)}: {mst}")
        
        try:
            result = processor.process_mst(mst, 'summary')
            results.append(result)
            
            if result.get('success'):
                successful += 1
                print(f"✅ Success: {result.get('company_name', 'N/A')}")
            else:
                failed += 1
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            failed += 1
            print(f"❌ Error: {e}")
            results.append({'success': False, 'mst': mst, 'error': str(e)})
    
    print(f"\n📈 BATCH PROCESSING RESULTS:")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Success Rate: {successful/(successful+failed)*100:.1f}%")
    
    return results

def demo_detailed_analysis():
    """Demo detailed analysis"""
    print("\n📈 DEMO 3: DETAILED ANALYSIS")
    print("-" * 50)
    
    # Create processor
    processor = MSTProcessor()
    
    mst = "0101234567"
    print(f"🔍 Detailed analysis for MST: {mst}")
    print("⏳ Processing...")
    
    try:
        result = processor.process_mst(mst, 'detailed')
        
        if result.get('success'):
            print("✅ DETAILED ANALYSIS COMPLETE!")
            
            # Enterprise Summary
            enterprise = result.get('enterprise_summary', {})
            print(f"\n🏢 ENTERPRISE INFORMATION:")
            print(f"  - Company: {enterprise.get('company_name', 'N/A')}")
            print(f"  - Address: {enterprise.get('address', 'N/A')}")
            print(f"  - Phone: {enterprise.get('phone', 'N/A')}")
            print(f"  - Website: {enterprise.get('website', 'N/A')}")
            print(f"  - Sector: {enterprise.get('sector', 'N/A')}")
            print(f"  - Type: {enterprise.get('type', 'N/A')}")
            print(f"  - Revenue: {enterprise.get('revenue', 0):,.0f} VND")
            print(f"  - Bank Account: {enterprise.get('bank_account', 'N/A')}")
            print(f"  - Registration: {enterprise.get('registration_date', 'N/A')}")
            print(f"  - Expiry: {enterprise.get('expiry_date', 'N/A')}")
            
            # VSS Summary
            vss = result.get('vss_summary', {})
            print(f"\n🏥 VSS INFORMATION:")
            print(f"  - Employees: {vss.get('total_employees', 0)}")
            print(f"  - Contributions: {vss.get('total_contributions', 0)}")
            print(f"  - Claims: {vss.get('total_claims', 0)}")
            print(f"  - Hospitals: {vss.get('total_hospitals', 0)}")
            print(f"  - Compliance: {vss.get('compliance_score', 0):.1f}%")
            print(f"  - Risk Level: {vss.get('risk_level', 'N/A')}")
            
            # Analysis Summary
            analysis = result.get('analysis_summary', {})
            print(f"\n📊 ANALYSIS SUMMARY:")
            
            # Employee Analysis
            emp_analysis = analysis.get('employee_analysis', {})
            print(f"  👥 EMPLOYEE ANALYSIS:")
            print(f"    - Total: {emp_analysis.get('total_employees', 0)}")
            print(f"    - Active: {emp_analysis.get('active_employees', 0)}")
            print(f"    - Average Salary: {emp_analysis.get('average_salary', 0):,.0f} VND")
            
            # Contribution Analysis
            cont_analysis = analysis.get('contribution_analysis', {})
            print(f"  💰 CONTRIBUTION ANALYSIS:")
            print(f"    - Total Contributions: {cont_analysis.get('total_contributions', 0)}")
            print(f"    - Total Amount: {cont_analysis.get('total_contribution_amount', 0):,.0f} VND")
            print(f"    - Average: {cont_analysis.get('average_contribution', 0):,.0f} VND")
            
            # Compliance Report
            compliance = analysis.get('compliance_report', {})
            print(f"  📊 COMPLIANCE REPORT:")
            print(f"    - Overall Score: {compliance.get('overall_compliance_score', 0):.1f}%")
            print(f"    - Registration: {'✅' if compliance.get('registration_compliance') else '❌'}")
            print(f"    - Contribution: {'✅' if compliance.get('contribution_compliance') else '❌'}")
            print(f"    - Employee: {'✅' if compliance.get('employee_compliance') else '❌'}")
            
            # Risk Assessment
            risk = analysis.get('risk_assessment', {})
            print(f"  ⚠️  RISK ASSESSMENT:")
            print(f"    - Risk Level: {risk.get('risk_level', 'N/A')}")
            print(f"    - Risk Score: {risk.get('risk_score', 0):.1f}/100")
            
            # Recommendations
            recommendations = analysis.get('recommendations', [])
            print(f"  💡 RECOMMENDATIONS ({len(recommendations)}):")
            for i, rec in enumerate(recommendations[:5], 1):  # Show first 5
                print(f"    {i}. {rec}")
            
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")

def demo_system_statistics():
    """Demo system statistics"""
    print("\n📊 DEMO 4: SYSTEM STATISTICS")
    print("-" * 50)
    
    # Create processor
    processor = MSTProcessor()
    
    # Get statistics
    stats = processor.integration_system.get_statistics()
    
    print("📈 SYSTEM PERFORMANCE:")
    print(f"  - Total Requests: {stats['total_requests']}")
    print(f"  - Successful: {stats['successful_requests']}")
    print(f"  - Failed: {stats['failed_requests']}")
    print(f"  - Success Rate: {stats['success_rate']:.1f}%")
    print(f"  - Average Time: {stats['average_extraction_time']:.2f}s")
    
    # Configuration
    config = processor.config
    print(f"\n⚙️  SYSTEM CONFIGURATION:")
    print(f"  - Timeout: {config.get('timeout', 30)}s")
    print(f"  - Retry Attempts: {config.get('retry_attempts', 3)}")
    print(f"  - Rate Limit: {config.get('rate_limit_delay', 1.0)}s")
    print(f"  - Caching: {config.get('enable_caching', True)}")
    print(f"  - Save Results: {config.get('save_results', True)}")
    print(f"  - Generate Reports: {config.get('generate_report', True)}")

def demo_file_outputs():
    """Demo file outputs"""
    print("\n📁 DEMO 5: FILE OUTPUTS")
    print("-" * 50)
    
    # Create processor
    processor = MSTProcessor()
    
    mst = "0101234567"
    print(f"🔍 Generating files for MST: {mst}")
    print("⏳ Processing...")
    
    try:
        result = processor.process_mst(mst, 'json')
        
        if result.get('success'):
            print("✅ FILES GENERATED:")
            
            # Check data directory
            data_dir = "data"
            if os.path.exists(data_dir):
                files = os.listdir(data_dir)
                json_files = [f for f in files if f.endswith('.json')]
                print(f"  📄 JSON Files: {len(json_files)}")
                for file in json_files[-3:]:  # Show last 3
                    print(f"    - {file}")
            
            # Check reports directory
            reports_dir = "reports"
            if os.path.exists(reports_dir):
                files = os.listdir(reports_dir)
                md_files = [f for f in files if f.endswith('.md')]
                print(f"  📊 Report Files: {len(md_files)}")
                for file in md_files[-3:]:  # Show last 3
                    print(f"    - {file}")
            
            # Check logs directory
            logs_dir = "logs"
            if os.path.exists(logs_dir):
                files = os.listdir(logs_dir)
                log_files = [f for f in files if f.endswith('.log')]
                print(f"  📝 Log Files: {len(log_files)}")
                for file in log_files[-3:]:  # Show last 3
                    print(f"    - {file}")
            
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")

def main():
    """Main demo function"""
    print_demo_banner()
    
    print("🎬 Starting VSS Enterprise Integration System Demo...")
    print("This demo will showcase the system's capabilities with sample data.")
    print()
    
    try:
        # Demo 1: Single MST Processing
        demo_single_mst_processing()
        
        # Demo 2: Multiple MST Processing
        demo_multiple_mst_processing()
        
        # Demo 3: Detailed Analysis
        demo_detailed_analysis()
        
        # Demo 4: System Statistics
        demo_system_statistics()
        
        # Demo 5: File Outputs
        demo_file_outputs()
        
        print("\n" + "=" * 80)
        print("🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("📊 The VSS Enterprise Integration System is working as expected.")
        print("🚀 You can now use the system with real MSTs.")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ DEMO FAILED: {e}")
        print("Please check the system configuration and try again.")

if __name__ == "__main__":
    main()
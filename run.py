#!/usr/bin/env python3
"""
VSS Enterprise Integration System - Main Runner
Quick start script for the VSS Enterprise Integration System
"""

import sys
import os
import json
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from mst_processor import MSTProcessor

def print_banner():
    """Print system banner"""
    print("=" * 80)
    print("🏢 VSS ENTERPRISE INTEGRATION SYSTEM v1.0.0")
    print("🎯 Input: MST (Tax Code) → Output: Comprehensive Analysis")
    print("=" * 80)
    print()

def print_menu():
    """Print main menu"""
    print("📋 MAIN MENU:")
    print("1. 🔍 Process single MST")
    print("2. 📊 Process multiple MSTs")
    print("3. 📈 View system statistics")
    print("4. ⚙️  System configuration")
    print("5. 📚 Help and documentation")
    print("6. 🚪 Exit")
    print()

def process_single_mst(processor):
    """Process single MST"""
    print("🔍 PROCESS SINGLE MST")
    print("-" * 40)
    
    mst = input("Enter MST (Tax Code): ").strip()
    
    if not mst:
        print("❌ MST cannot be empty")
        return
    
    print(f"\n🚀 Processing MST: {mst}")
    print("⏳ Please wait...")
    
    try:
        result = processor.process_mst(mst, 'detailed')
        
        if result.get('success'):
            print("\n✅ PROCESSING SUCCESSFUL!")
            print(f"📊 Company: {result.get('enterprise_summary', {}).get('company_name', 'N/A')}")
            print(f"🏭 Sector: {result.get('enterprise_summary', {}).get('sector', 'N/A')}")
            print(f"💰 Revenue: {result.get('enterprise_summary', {}).get('revenue', 0):,.0f} VND")
            print(f"👥 Employees: {result.get('vss_summary', {}).get('total_employees', 0)}")
            print(f"📊 Compliance: {result.get('vss_summary', {}).get('compliance_score', 0):.1f}%")
            print(f"⚠️  Risk Level: {result.get('vss_summary', {}).get('risk_level', 'N/A')}")
            print(f"⏱️  Processing Time: {result.get('extraction_time', 0):.2f}s")
        else:
            print(f"\n❌ PROCESSING FAILED: {result.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

def process_multiple_msts(processor):
    """Process multiple MSTs"""
    print("📊 PROCESS MULTIPLE MSTs")
    print("-" * 40)
    
    msts_input = input("Enter MSTs (comma-separated): ").strip()
    
    if not msts_input:
        print("❌ MSTs cannot be empty")
        return
    
    msts = [mst.strip() for mst in msts_input.split(',')]
    
    print(f"\n🚀 Processing {len(msts)} MSTs...")
    print("⏳ Please wait...")
    
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
    
    print(f"\n📈 BATCH PROCESSING COMPLETE:")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Success Rate: {successful/(successful+failed)*100:.1f}%")

def view_statistics(processor):
    """View system statistics"""
    print("📈 SYSTEM STATISTICS")
    print("-" * 40)
    
    stats = processor.integration_system.get_statistics()
    
    print(f"📊 Total Requests: {stats['total_requests']}")
    print(f"✅ Successful Requests: {stats['successful_requests']}")
    print(f"❌ Failed Requests: {stats['failed_requests']}")
    print(f"📈 Success Rate: {stats['success_rate']:.1f}%")
    print(f"⏱️  Average Processing Time: {stats['average_extraction_time']:.2f}s")
    
    if stats['total_requests'] > 0:
        print(f"\n📊 RECENT ACTIVITY:")
        print(f"Last processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def system_configuration(processor):
    """System configuration"""
    print("⚙️  SYSTEM CONFIGURATION")
    print("-" * 40)
    
    config = processor.config
    
    print(f"🔧 Current Configuration:")
    print(f"  - Timeout: {config.get('timeout', 30)}s")
    print(f"  - Retry Attempts: {config.get('retry_attempts', 3)}")
    print(f"  - Rate Limit Delay: {config.get('rate_limit_delay', 1.0)}s")
    print(f"  - Enable Caching: {config.get('enable_caching', True)}")
    print(f"  - Cache Duration: {config.get('cache_duration', 3600)}s")
    print(f"  - Save Results: {config.get('save_results', True)}")
    print(f"  - Generate Report: {config.get('generate_report', True)}")
    
    print(f"\n📁 Directories:")
    print(f"  - Data: {os.path.join(os.getcwd(), 'data')}")
    print(f"  - Reports: {os.path.join(os.getcwd(), 'reports')}")
    print(f"  - Logs: {os.path.join(os.getcwd(), 'logs')}")

def help_documentation():
    """Help and documentation"""
    print("📚 HELP AND DOCUMENTATION")
    print("-" * 40)
    
    print("🔍 HOW TO USE:")
    print("1. Enter MST (Tax Code) to process")
    print("2. System will extract enterprise and VSS data")
    print("3. Results will be displayed and saved")
    
    print("\n📊 OUTPUT FORMATS:")
    print("- JSON: Complete data in JSON format")
    print("- Summary: Key information summary")
    print("- Detailed: Comprehensive analysis report")
    
    print("\n📁 OUTPUT FILES:")
    print("- Data: data/vss_integration_result_[MST]_[timestamp].json")
    print("- Reports: reports/vss_integration_report_[MST]_[timestamp].md")
    print("- Logs: logs/mst_processor.log")
    
    print("\n🔧 CONFIGURATION:")
    print("- File: config/system_config.json")
    print("- API endpoints, timeouts, caching settings")
    
    print("\n❓ COMMON ISSUES:")
    print("- Invalid MST: Check format (10-13 digits)")
    print("- API timeout: Increase timeout in config")
    print("- Network error: Check internet connection")
    
    print("\n📞 SUPPORT:")
    print("- Documentation: README.md")
    print("- Configuration: config/system_config.json")
    print("- Logs: logs/mst_processor.log")

def main():
    """Main function"""
    print_banner()
    
    # Create processor
    try:
        processor = MSTProcessor()
        print("✅ System initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize system: {e}")
        return
    
    while True:
        print_menu()
        
        try:
            choice = input("Select option (1-6): ").strip()
            
            if choice == '1':
                process_single_mst(processor)
            elif choice == '2':
                process_multiple_msts(processor)
            elif choice == '3':
                view_statistics(processor)
            elif choice == '4':
                system_configuration(processor)
            elif choice == '5':
                help_documentation()
            elif choice == '6':
                print("\n👋 Thank you for using VSS Enterprise Integration System!")
                print("🚀 Goodbye!")
                break
            else:
                print("❌ Invalid option. Please select 1-6.")
            
            input("\nPress Enter to continue...")
            print("\n" + "="*80 + "\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Test script to verify API connection and basic functionality.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from resume_processor import ResumeProcessor

def test_api_connection():
    """Test basic API connection."""
    print("🧪 Testing API Connection...")
    
    # Get API key
    api_key = os.environ.get("CEREBRAS_API_KEY")
    if not api_key:
        print("❌ Error: CEREBRAS_API_KEY environment variable not set")
        print("Please set it with: export CEREBRAS_API_KEY='your_api_key_here'")
        return False
    
    try:
        # Initialize processor
        processor = ResumeProcessor(api_key)
        print("✅ Processor initialized successfully")
        
        # Test with simple resume text
        test_resume = """
        张三，男，清华大学计算机科学硕士学位，2020年毕业。
        曾在阿里巴巴担任软件工程师，2020年-2022年。
        获得优秀员工奖。
        """
        
        print("🔄 Testing resume extraction...")
        result = processor.extract_resume_info(test_resume, "测试用户")
        
        if result and 'basic_info' in result:
            print("✅ API test successful!")
            print("📊 Sample result:")
            print(f"  Gender: {result['basic_info'].get('gender', 'N/A')}")
            print(f"  Education: {result['basic_info'].get('education', 'N/A')}")
            print(f"  School: {result['basic_info'].get('graduate_school', 'N/A')}")
            return True
        else:
            print("❌ API test failed: Invalid response format")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {str(e)}")
        return False

def test_dependencies():
    """Test if all required dependencies are installed."""
    print("📦 Testing Dependencies...")
    
    try:
        import pandas
        print("✅ pandas imported successfully")
    except ImportError:
        print("❌ pandas not found. Install with: pip install pandas")
        return False
    
    try:
        import openpyxl
        print("✅ openpyxl imported successfully")
    except ImportError:
        print("❌ openpyxl not found. Install with: pip install openpyxl")
        return False
    
    try:
        from cerebras.cloud.sdk import Cerebras
        print("✅ cerebras-cloud-sdk imported successfully")
    except ImportError:
        print("❌ cerebras-cloud-sdk not found. Install with: pip install cerebras-cloud-sdk")
        return False
    
    return True

def main():
    """Run all tests."""
    print("🚀 Running Fund Manager Resume Processor Tests")
    print("=" * 50)
    
    # Test dependencies
    deps_ok = test_dependencies()
    if not deps_ok:
        print("\n❌ Dependency tests failed. Please install missing packages.")
        return False
    
    print("\n" + "=" * 50)
    
    # Test API connection
    api_ok = test_api_connection()
    if not api_ok:
        print("\n❌ API tests failed. Please check your configuration.")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Your setup is ready to use.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


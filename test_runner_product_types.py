# fixed_test_runner_product_types.py
"""
Fixed test runner script for Product Types page automation tests
"""

import pytest
import sys
import os
from datetime import datetime

def run_product_types_tests():
    """Run all product types page tests with comprehensive reporting"""

    # Test execution arguments
    pytest_args = [
        "tests/test_product_types_page.py",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--html=reports/product_types_test_report.html",  # HTML report
        "--self-contained-html",  # Embed CSS/JS in HTML
        "--capture=no",  # Show print statements
        "-s",  # Don't capture output (shows setup steps)
        "--durations=10",  # Show slowest 10 tests
    ]

    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    print("🚀 Starting Product Types Page Automation Tests...")
    print(f"📅 Test execution started at: {datetime.now()}")
    print("🔐 Tests will include automatic authentication")
    print("-" * 80)

    # Run tests
    exit_code = pytest.main(pytest_args)

    print("-" * 80)
    print(f"✅ Test execution completed at: {datetime.now()}")
    print(f"📊 Exit code: {exit_code}")
    print("📁 Report saved: reports/product_types_test_report.html")

    return exit_code

def run_smoke_tests():
    """Run only smoke tests for quick verification"""
    pytest_args = [
        "tests/test_product_types_page.py",
        "-v",
        "-s",
        "-m", "smoke",
        "--html=reports/product_types_smoke_report.html",
        "--self-contained-html",
        "--tb=short"
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔥 Running Product Types Smoke Tests...")
    print("⚡ This will test core functionality quickly")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Smoke tests completed with exit code: {exit_code}")
    return exit_code

def run_security_tests():
    """Run only security tests"""
    pytest_args = [
        "tests/test_product_types_page.py",
        "-v",
        "-s",
        "-m", "security",
        "--html=reports/product_types_security_report.html",
        "--self-contained-html",
        "--tb=long"  # Longer traceback for security issues
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔒 Running Product Types Security Tests...")
    print("🛡️  Testing XSS, SQL injection, and HTML injection protection")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Security tests completed with exit code: {exit_code}")
    return exit_code

def run_regression_tests():
    """Run regression tests"""
    pytest_args = [
        "tests/test_product_types_page.py",
        "-v",
        "-s",
        "-m", "regression",
        "--html=reports/product_types_regression_report.html",
        "--self-contained-html",
        "--tb=short",
        "--durations=20"  # Show more timing info for regression
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔄 Running Product Types Regression Tests...")
    print("📋 Testing all major functionality comprehensively")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Regression tests completed with exit code: {exit_code}")
    return exit_code

def run_with_browser(browser_name):
    """Run tests with specific browser"""
    pytest_args = [
        "tests/test_product_types_page.py",
        "-v",
        "-s",
        f"--browser={browser_name}",
        "--html=reports/product_types_browser_test_report.html",
        "--self-contained-html",
        "-m", "smoke"  # Run smoke tests for browser compatibility
    ]

    os.makedirs("reports", exist_ok=True)

    print(f"🌐 Running Product Types tests with {browser_name.upper()} browser...")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ {browser_name.upper()} tests completed with exit code: {exit_code}")
    return exit_code

def run_headless_tests():
    """Run tests in headless mode"""
    pytest_args = [
        "tests/test_product_types_page.py",
        "-v",
        "--headless",
        "--html=reports/product_types_headless_report.html",
        "--self-contained-html",
        "-m", "smoke"
    ]

    os.makedirs("reports", exist_ok=True)

    print("👻 Running Product Types tests in HEADLESS mode...")
    print("🖥️  No browser window will be displayed")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Headless tests completed with exit code: {exit_code}")
    return exit_code

def print_usage():
    """Print usage instructions"""
    print("""
🧪 Fixed Test Runner for Product Types Page

Usage: python fixed_test_runner_product_types.py [OPTIONS]

Available Commands:
    all         - Run all product types tests (default)
    smoke       - Run smoke tests (quick verification)
    security    - Run security tests (XSS, SQL injection, etc.)
    regression  - Run comprehensive regression tests
    chrome      - Run smoke tests with Chrome browser
    firefox     - Run smoke tests with Firefox browser
    edge        - Run smoke tests with Edge browser
    headless    - Run smoke tests in headless mode

Examples:
    python fixed_test_runner_product_types.py                # Run all tests
    python fixed_test_runner_product_types.py smoke          # Quick smoke tests
    python fixed_test_runner_product_types.py security       # Security-focused tests
    python fixed_test_runner_product_types.py chrome         # Test with Chrome
    python fixed_test_runner_product_types.py headless       # Test without GUI

Features:
    ✅ Automatic login with admin@shopizer.com
    ✅ Automatic language change from French to English
    ✅ Fixed ChromeDriver emoji compatibility issues
    ✅ Simplified sorting logic based on product groups page
    ✅ Comprehensive error handling and screenshots
    ✅ Detailed HTML reports with embedded media

Test Categories:
    🔥 smoke      - Core functionality verification
    🔒 security   - Security vulnerability testing
    🔄 regression - Comprehensive feature testing
    🎨 ui         - User interface interaction testing

Reports Location: ./reports/
Screenshots Location: ./screenshots/

Fixed Issues:
    ❌ ChromeDriver emoji support - Removed emoji tests
    ❌ Complex sorting logic - Simplified based on working product groups
    ❌ Inconsistent locators - Updated to CSS selectors
    ❌ Timeout issues - Added proper waits and error handling
    """)

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "smoke":
            exit_code = run_smoke_tests()
        elif command == "security":
            exit_code = run_security_tests()
        elif command == "regression":
            exit_code = run_regression_tests()
        elif command == "chrome":
            exit_code = run_with_browser("chrome")
        elif command == "firefox":
            exit_code = run_with_browser("firefox")
        elif command == "edge":
            exit_code = run_with_browser("edge")
        elif command == "headless":
            exit_code = run_headless_tests()
        elif command == "all":
            exit_code = run_product_types_tests()
        elif command in ["help", "-h", "--help"]:
            print_usage()
            exit_code = 0
        else:
            print(f"❌ Unknown command: {command}")
            print_usage()
            exit_code = 1
    else:
        exit_code = run_product_types_tests()

    if exit_code == 0:
        print("\n🎉 All tests completed successfully!")
    else:
        print(f"\n❌ Tests completed with {exit_code} failures")
        print("🔍 Check the HTML report for detailed results")

    sys.exit(exit_code)
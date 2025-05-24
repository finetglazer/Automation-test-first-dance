# test_runner_brands.py
"""
Test runner script for Brands page automation tests
"""

import pytest
import sys
import os
from datetime import datetime

def run_brands_tests():
    """Run all brands page tests with comprehensive reporting"""

    # Test execution arguments
    pytest_args = [
        "tests/test_brands_page.py",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--html=reports/brands_test_report.html",  # HTML report
        "--self-contained-html",  # Embed CSS/JS in HTML
        "--capture=no",  # Show print statements
        "-s",  # Don't capture output (shows setup steps)
        "--durations=10",  # Show slowest 10 tests
    ]

    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    print("🚀 Starting Brands Page Automation Tests...")
    print(f"📅 Test execution started at: {datetime.now()}")
    print("🔐 Tests will include automatic authentication")
    print("🏷️ Testing Brands page with dual search functionality")
    print("-" * 80)

    # Run tests
    exit_code = pytest.main(pytest_args)

    print("-" * 80)
    print(f"✅ Test execution completed at: {datetime.now()}")
    print(f"📊 Exit code: {exit_code}")
    print("📁 Report saved: reports/brands_test_report.html")

    return exit_code

def run_smoke_tests():
    """Run only smoke tests for quick verification"""
    pytest_args = [
        "tests/test_brands_page.py",
        "-v",
        "-s",
        "-m", "smoke",
        "--html=reports/brands_smoke_report.html",
        "--self-contained-html",
        "--tb=short"
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔥 Running Brands Smoke Tests...")
    print("⚡ This will test core functionality quickly")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Smoke tests completed with exit code: {exit_code}")
    return exit_code

def run_security_tests():
    """Run only security tests"""
    pytest_args = [
        "tests/test_brands_page.py",
        "-v",
        "-s",
        "-m", "security",
        "--html=reports/brands_security_report.html",
        "--self-contained-html",
        "--tb=long"  # Longer traceback for security issues
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔒 Running Brands Security Tests...")
    print("🛡️  Testing XSS, SQL injection, and HTML injection protection")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Security tests completed with exit code: {exit_code}")
    return exit_code

def run_regression_tests():
    """Run regression tests"""
    pytest_args = [
        "tests/test_brands_page.py",
        "-v",
        "-s",
        "-m", "regression",
        "--html=reports/brands_regression_report.html",
        "--self-contained-html",
        "--tb=short",
        "--durations=20"  # Show more timing info for regression
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔄 Running Brands Regression Tests...")
    print("📋 Testing all major functionality comprehensively")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Regression tests completed with exit code: {exit_code}")
    return exit_code

def run_ui_tests():
    """Run UI-specific tests"""
    pytest_args = [
        "tests/test_brands_page.py",
        "-v",
        "-s",
        "-m", "ui",
        "--html=reports/brands_ui_report.html",
        "--self-contained-html",
        "--tb=short"
    ]

    os.makedirs("reports", exist_ok=True)

    print("🎨 Running Brands UI Tests...")
    print("🖱️  Testing user interface interactions")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ UI tests completed with exit code: {exit_code}")
    return exit_code

def run_with_browser(browser_name):
    """Run tests with specific browser"""
    pytest_args = [
        "tests/test_brands_page.py",
        "-v",
        "-s",
        f"--browser={browser_name}",
        "--html=reports/brands_browser_test_report.html",
        "--self-contained-html",
        "-m", "smoke"  # Run smoke tests for browser compatibility
    ]

    os.makedirs("reports", exist_ok=True)

    print(f"🌐 Running Brands tests with {browser_name.upper()} browser...")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ {browser_name.upper()} tests completed with exit code: {exit_code}")
    return exit_code

def run_headless_tests():
    """Run tests in headless mode"""
    pytest_args = [
        "tests/test_brands_page.py",
        "-v",
        "--headless",
        "--html=reports/brands_headless_report.html",
        "--self-contained-html",
        "-m", "smoke"
    ]

    os.makedirs("reports", exist_ok=True)

    print("👻 Running Brands tests in HEADLESS mode...")
    print("🖥️  No browser window will be displayed")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Headless tests completed with exit code: {exit_code}")
    return exit_code

def print_usage():
    """Print usage instructions"""
    print("""
🧪 Test Runner for Brands Page with Dual Search Functionality

Usage: python test_runner_brands.py [OPTIONS]

Available Commands:
    all         - Run all brands tests (default)
    smoke       - Run smoke tests (quick verification)
    security    - Run security tests (XSS, SQL injection, etc.)
    regression  - Run comprehensive regression tests
    ui          - Run UI interaction tests
    chrome      - Run smoke tests with Chrome browser
    firefox     - Run smoke tests with Firefox browser
    edge        - Run smoke tests with Edge browser
    headless    - Run smoke tests in headless mode

Examples:
    python test_runner_brands.py                # Run all tests
    python test_runner_brands.py smoke          # Quick smoke tests
    python test_runner_brands.py security       # Security-focused tests
    python test_runner_brands.py ui             # UI interaction tests
    python test_runner_brands.py chrome         # Test with Chrome
    python test_runner_brands.py headless       # Test without GUI

Features:
    ✅ Automatic login with admin@shopizer.com
    ✅ Automatic language change from French to English
    ✅ Dual search functionality testing (general + table filters)
    ✅ Search and Reset button testing
    ✅ Comprehensive error handling and screenshots
    ✅ Detailed HTML reports with embedded media

Test Categories:
    🔥 smoke      - Core functionality verification
    🔒 security   - Security vulnerability testing
    🔄 regression - Comprehensive feature testing
    🎨 ui         - User interface interaction testing

Special Brands Page Features:
    🔍 General search field with search/reset buttons
    📋 Table-specific filters (Brand Name, Code)
    🏷️ Brand-specific data validation
    📊 Pagination testing
    ⚡ Dual search mechanism validation

Reports Location: ./reports/
Screenshots Location: ./screenshots/

Test Coverage:
    ✅ Special character input validation
    ✅ Valid/invalid text searching
    ✅ Leading/trailing spaces handling
    ✅ Security injection protection
    ✅ Large value input testing
    ✅ Column sorting (ascending/descending/default)
    ✅ Multiple column sorting
    ✅ Combined filter and sort operations
    ✅ Page reset functionality
    ✅ Search/Reset button functionality
    ✅ Action buttons verification
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
        elif command == "ui":
            exit_code = run_ui_tests()
        elif command == "chrome":
            exit_code = run_with_browser("chrome")
        elif command == "firefox":
            exit_code = run_with_browser("firefox")
        elif command == "edge":
            exit_code = run_with_browser("edge")
        elif command == "headless":
            exit_code = run_headless_tests()
        elif command == "all":
            exit_code = run_brands_tests()
        elif command in ["help", "-h", "--help"]:
            print_usage()
            exit_code = 0
        else:
            print(f"❌ Unknown command: {command}")
            print_usage()
            exit_code = 1
    else:
        exit_code = run_brands_tests()

    if exit_code == 0:
        print("\n🎉 All tests completed successfully!")
    else:
        print(f"\n❌ Tests completed with {exit_code} failures")
        print("🔍 Check the HTML report for detailed results")

    sys.exit(exit_code)
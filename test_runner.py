# test_runner.py
"""
Enhanced test runner script for Products page automation tests with authentication
"""

import pytest
import sys
import os
from datetime import datetime

def run_products_tests():
    """Run all products page tests with comprehensive reporting"""

    # Test execution arguments
    pytest_args = [
        "tests/test_products_page.py",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--html=reports/products_test_report.html",  # HTML report
        "--self-contained-html",  # Embed CSS/JS in HTML
        "--capture=no",  # Show print statements
        "-s",  # Don't capture output (shows authentication steps)
        "-m", "not slow",  # Skip slow tests (if any)
        "--durations=10",  # Show slowest 10 tests
    ]

    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    print("🚀 Starting Products Page Automation Tests with Authentication...")
    print(f"📅 Test execution started at: {datetime.now()}")
    print("🔐 Tests will include automatic login and language setup")
    print("-" * 80)

    # Run tests
    exit_code = pytest.main(pytest_args)

    print("-" * 80)
    print(f"✅ Test execution completed at: {datetime.now()}")
    print(f"📊 Exit code: {exit_code}")
    print("📁 Report saved: reports/products_test_report.html")

    return exit_code

def run_smoke_tests():
    """Run only smoke tests for quick verification"""
    pytest_args = [
        "tests/test_products_page.py",
        "-v",
        "-s",
        "-m", "smoke",
        "--html=reports/smoke_test_report.html",
        "--self-contained-html",
        "--tb=short"
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔥 Running Smoke Tests with Authentication...")
    print("⚡ This will test core functionality quickly")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Smoke tests completed with exit code: {exit_code}")
    return exit_code

def run_security_tests():
    """Run only security tests"""
    pytest_args = [
        "tests/test_products_page.py",
        "-v",
        "-s",
        "-m", "security",
        "--html=reports/security_test_report.html",
        "--self-contained-html",
        "--tb=long"  # Longer traceback for security issues
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔒 Running Security Tests...")
    print("🛡️  Testing XSS, SQL injection, and HTML injection protection")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Security tests completed with exit code: {exit_code}")
    return exit_code

def run_regression_tests():
    """Run regression tests"""
    pytest_args = [
        "tests/test_products_page.py",
        "-v",
        "-s",
        "-m", "regression",
        "--html=reports/regression_test_report.html",
        "--self-contained-html",
        "--tb=short",
        "--durations=20"  # Show more timing info for regression
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔄 Running Regression Tests...")
    print("📋 Testing all major functionality comprehensively")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Regression tests completed with exit code: {exit_code}")
    return exit_code

def run_authentication_tests():
    """Run authentication-specific tests"""
    pytest_args = [
        "tests/test_products_page.py::TestAuthentication",
        "-v",
        "-s",
        "--html=reports/authentication_test_report.html",
        "--self-contained-html",
        "--tb=long"
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔐 Running Authentication Tests...")
    print("👤 Testing login flow and language change functionality")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Authentication tests completed with exit code: {exit_code}")
    return exit_code

def run_with_browser(browser_name):
    """Run tests with specific browser"""
    pytest_args = [
        "tests/test_products_page.py",
        "-v",
        "-s",
        f"--browser={browser_name}",
        "--html=reports/browser_test_report.html",
        "--self-contained-html",
        "-m", "smoke"  # Run smoke tests for browser compatibility
    ]

    os.makedirs("reports", exist_ok=True)

    print(f"🌐 Running tests with {browser_name.upper()} browser...")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ {browser_name.upper()} tests completed with exit code: {exit_code}")
    return exit_code

def run_headless_tests():
    """Run tests in headless mode"""
    pytest_args = [
        "tests/test_products_page.py",
        "-v",
        "--headless",
        "--html=reports/headless_test_report.html",
        "--self-contained-html",
        "-m", "smoke"
    ]

    os.makedirs("reports", exist_ok=True)

    print("👻 Running tests in HEADLESS mode...")
    print("🖥️  No browser window will be displayed")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Headless tests completed with exit code: {exit_code}")
    return exit_code

def print_usage():
    """Print usage instructions"""
    print("""
🧪 Enhanced Test Runner for Products Page with Authentication

Usage: python test_runner.py [OPTIONS]

Available Commands:
    all         - Run all product page tests (default)
    smoke       - Run smoke tests (quick verification)
    security    - Run security tests (XSS, SQL injection, etc.)
    regression  - Run comprehensive regression tests
    auth        - Run authentication-specific tests
    chrome      - Run smoke tests with Chrome browser
    firefox     - Run smoke tests with Firefox browser
    edge        - Run smoke tests with Edge browser
    headless    - Run smoke tests in headless mode

Examples:
    python test_runner.py                # Run all tests
    python test_runner.py smoke          # Quick smoke tests
    python test_runner.py security       # Security-focused tests
    python test_runner.py chrome         # Test with Chrome
    python test_runner.py headless       # Test without GUI

Features:
    ✅ Automatic login with admin@shopizer.com
    ✅ Automatic language change from French to English
    ✅ Comprehensive error handling and screenshots
    ✅ Detailed HTML reports with embedded media
    ✅ Support for multiple browsers
    ✅ Authentication flow testing

Test Categories:
    🔥 smoke      - Core functionality verification
    🔒 security   - Security vulnerability testing
    🔄 regression - Comprehensive feature testing
    🎨 ui         - User interface interaction testing

Reports Location: ./reports/
Screenshots Location: ./screenshots/
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
        elif command == "auth":
            exit_code = run_authentication_tests()
        elif command == "chrome":
            exit_code = run_with_browser("chrome")
        elif command == "firefox":
            exit_code = run_with_browser("firefox")
        elif command == "edge":
            exit_code = run_with_browser("edge")
        elif command == "headless":
            exit_code = run_headless_tests()
        elif command == "all":
            exit_code = run_products_tests()
        elif command in ["help", "-h", "--help"]:
            print_usage()
            exit_code = 0
        else:
            print(f"❌ Unknown command: {command}")
            print_usage()
            exit_code = 1
    else:
        exit_code = run_products_tests()

    if exit_code == 0:
        print("\n🎉 All tests completed successfully!")
    else:
        print(f"\n❌ Tests completed with {exit_code} failures")
        print("🔍 Check the HTML report for detailed results")

    sys.exit(exit_code)


# Additional utility script: quick_test.py
"""
Quick test script for debugging authentication issues
Save as: quick_test.py
"""

def quick_authentication_test():
    """Quick test to verify authentication works"""
    from selenium import webdriver
    from utils.driver_factory import DriverFactory
    from pages.login_page import LoginPage
    from pages.home_page import HomePage
    from pages.products_page import ProductsPage
    import time

    print("🔧 Quick Authentication Test")
    print("-" * 40)

    driver = None
    try:
        # Create driver
        driver = DriverFactory.get_driver("chrome", headless=False)
        driver.implicitly_wait(10)

        # Test login
        print("1️⃣ Testing login...")
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page("http://localhost")

        if login_page.is_login_page_loaded():
            print("✅ Login page loaded")
        else:
            print("❌ Login page failed to load")
            return

        # Perform login
        if login_page.perform_login("admin@shopizer.com", "password"):
            print("✅ Login successful")
        else:
            print("❌ Login failed")
            return

        # Test language change
        print("2️⃣ Testing language change...")
        home_page = HomePage(driver)
        home_page.wait_for_home_page_load()

        current_lang = home_page.get_current_language()
        print(f"Current language: {current_lang}")

        if home_page.is_french_language():
            if home_page.change_language_to_english():
                print("✅ Language changed to English")
            else:
                print("⚠️ Could not change language")
        else:
            print("✅ Language is already acceptable")

        # Test products page
        print("3️⃣ Testing products page navigation...")
        products_page = ProductsPage(driver)

        if products_page.navigate_to_products_page():
            print("✅ Products page navigation successful")

            # Quick verification
            if products_page.is_element_visible(products_page.SKU_SEARCH_INPUT):
                print("✅ Products page elements visible")
            else:
                print("❌ Products page elements not found")
        else:
            print("❌ Products page navigation failed")

        print("\n✅ Quick authentication test completed!")
        time.sleep(3)  # Keep browser open briefly

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # This section only runs if you execute this file directly as quick_test.py
    quick_authentication_test()
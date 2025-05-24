# test_runner_options_set.py
"""
Test runner script for Options Set page automation tests
Focused on sorting functionality and table interactions
"""

import pytest
import sys
import os
from datetime import datetime

def run_options_set_tests():
    """Run all options set page tests with comprehensive reporting"""

    # Test execution arguments
    pytest_args = [
        "tests/test_options_set_page.py",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--html=reports/options_set_test_report.html",  # HTML report
        "--self-contained-html",  # Embed CSS/JS in HTML
        "--capture=no",  # Show print statements
        "-s",  # Don't capture output (shows setup steps)
        "--durations=10",  # Show slowest 10 tests
    ]

    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    print("🚀 Starting Options Set Page Automation Tests...")
    print(f"📅 Test execution started at: {datetime.now()}")
    print("⚙️ Focus: Sorting functionality and table interactions")
    print("🔐 Tests will include automatic authentication")
    print("-" * 80)

    # Run tests
    exit_code = pytest.main(pytest_args)

    print("-" * 80)
    print(f"✅ Test execution completed at: {datetime.now()}")
    print(f"📊 Exit code: {exit_code}")
    print("📁 Report saved: reports/options_set_test_report.html")

    return exit_code

def run_smoke_tests():
    """Run only smoke tests for quick verification"""
    pytest_args = [
        "tests/test_options_set_page.py",
        "-v",
        "-s",
        "-m", "smoke",
        "--html=reports/options_set_smoke_report.html",
        "--self-contained-html",
        "--tb=short"
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔥 Running Options Set Smoke Tests...")
    print("⚡ This will test core functionality quickly")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Smoke tests completed with exit code: {exit_code}")
    return exit_code

def run_regression_tests():
    """Run comprehensive regression tests"""
    pytest_args = [
        "tests/test_options_set_page.py",
        "-v",
        "-s",
        "-m", "regression",
        "--html=reports/options_set_regression_report.html",
        "--self-contained-html",
        "--tb=short",
        "--durations=20"  # Show more timing info for regression
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔄 Running Options Set Regression Tests...")
    print("📋 Testing all sorting functionality comprehensively")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Regression tests completed with exit code: {exit_code}")
    return exit_code

def run_ui_tests():
    """Run UI-focused tests"""
    pytest_args = [
        "tests/test_options_set_page.py",
        "-v",
        "-s",
        "-m", "ui",
        "--html=reports/options_set_ui_report.html",
        "--self-contained-html",
        "--tb=short"
    ]

    os.makedirs("reports", exist_ok=True)

    print("🎨 Running Options Set UI Tests...")
    print("🖱️  Testing user interface interactions")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ UI tests completed with exit code: {exit_code}")
    return exit_code

def run_stress_tests():
    """Run stress tests for sorting functionality"""
    pytest_args = [
        "tests/test_options_set_page.py::TestOptionsSetPageStressTest",
        "-v",
        "-s",
        "--html=reports/options_set_stress_report.html",
        "--self-contained-html",
        "--tb=long"
    ]

    os.makedirs("reports", exist_ok=True)

    print("💪 Running Options Set Stress Tests...")
    print("🔄 Testing rapid sorting changes and stability")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Stress tests completed with exit code: {exit_code}")
    return exit_code

def run_with_browser(browser_name):
    """Run tests with specific browser"""
    pytest_args = [
        "tests/test_options_set_page.py",
        "-v",
        "-s",
        f"--browser={browser_name}",
        "--html=reports/options_set_browser_test_report.html",
        "--self-contained-html",
        "-m", "smoke"  # Run smoke tests for browser compatibility
    ]

    os.makedirs("reports", exist_ok=True)

    print(f"🌐 Running Options Set tests with {browser_name.upper()} browser...")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ {browser_name.upper()} tests completed with exit code: {exit_code}")
    return exit_code

def run_headless_tests():
    """Run tests in headless mode"""
    pytest_args = [
        "tests/test_options_set_page.py",
        "-v",
        "--headless",
        "--html=reports/options_set_headless_report.html",
        "--self-contained-html",
        "-m", "smoke"
    ]

    os.makedirs("reports", exist_ok=True)

    print("👻 Running Options Set tests in HEADLESS mode...")
    print("🖥️  No browser window will be displayed")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Headless tests completed with exit code: {exit_code}")
    return exit_code

def run_sorting_tests_only():
    """Run only sorting-specific tests"""
    pytest_args = [
        "tests/test_options_set_page.py::TestOptionsSetPageSorting",
        "-v",
        "-s",
        "--html=reports/options_set_sorting_report.html",
        "--self-contained-html",
        "--tb=short"
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔢 Running Options Set Sorting Tests Only...")
    print("📊 Focus: All sorting functionality")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Sorting tests completed with exit code: {exit_code}")
    return exit_code

def print_usage():
    """Print usage instructions"""
    print("""
⚙️ Test Runner for Options Set / Property Set Page

Usage: python test_runner_options_set.py [OPTIONS]

Available Commands:
    all         - Run all options set tests (default)
    smoke       - Run smoke tests (quick verification)
    regression  - Run comprehensive regression tests
    ui          - Run UI interaction tests
    stress      - Run stress tests (rapid sorting changes)
    sorting     - Run sorting tests only
    chrome      - Run smoke tests with Chrome browser
    firefox     - Run smoke tests with Firefox browser
    edge        - Run smoke tests with Edge browser
    headless    - Run smoke tests in headless mode

Examples:
    python test_runner_options_set.py                # Run all tests
    python test_runner_options_set.py smoke          # Quick smoke tests
    python test_runner_options_set.py sorting        # Sorting functionality only
    python test_runner_options_set.py stress         # Stress test sorting
    python test_runner_options_set.py chrome         # Test with Chrome
    python test_runner_options_set.py headless       # Test without GUI

Features:
    ✅ Automatic login with admin@shopizer.com
    ✅ Automatic language change from French to English
    ✅ Comprehensive sorting functionality testing
    ✅ Table structure validation
    ✅ Action button verification
    ✅ Stress testing for rapid changes
    ✅ Detailed HTML reports with embedded media

Test Categories:
    🔥 smoke      - Core functionality verification
    🔄 regression - Comprehensive feature testing  
    🎨 ui         - User interface interaction testing
    💪 stress     - Stability under rapid changes

Page Focus:
    📊 Primary: Sorting functionality (all 5 columns)
    🏗️ Secondary: Table structure and integrity
    🔘 Tertiary: Action buttons (Create, Edit, Delete)

Reports Location: ./reports/
Screenshots Location: ./screenshots/

URL: http://localhost/#/pages/catalogue/options/options-set-list
Columns: ID, Code, Option name, Option value/property, Product types, Action
    """)

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "smoke":
            exit_code = run_smoke_tests()
        elif command == "regression":
            exit_code = run_regression_tests()
        elif command == "ui":
            exit_code = run_ui_tests()
        elif command == "stress":
            exit_code = run_stress_tests()
        elif command == "sorting":
            exit_code = run_sorting_tests_only()
        elif command == "chrome":
            exit_code = run_with_browser("chrome")
        elif command == "firefox":
            exit_code = run_with_browser("firefox")
        elif command == "edge":
            exit_code = run_with_browser("edge")
        elif command == "headless":
            exit_code = run_headless_tests()
        elif command == "all":
            exit_code = run_options_set_tests()
        elif command in ["help", "-h", "--help"]:
            print_usage()
            exit_code = 0
        else:
            print(f"❌ Unknown command: {command}")
            print_usage()
            exit_code = 1
    else:
        exit_code = run_options_set_tests()

    if exit_code == 0:
        print("\n🎉 All tests completed successfully!")
        print("📊 Options Set page sorting functionality verified!")
    else:
        print(f"\n❌ Tests completed with {exit_code} failures")
        print("🔍 Check the HTML report for detailed results")

    sys.exit(exit_code)
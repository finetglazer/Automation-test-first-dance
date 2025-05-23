# simplified_test_runner_product_groups.py
"""
Simplified test runner script for Product Groups page automation tests
"""

import pytest
import sys
import os
from datetime import datetime

def run_product_groups_tests():
    """Run all product groups page tests with simple reporting"""

    # Test execution arguments
    pytest_args = [
        "tests/test_product_groups_page.py",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--html=reports/product_groups_test_report.html",  # HTML report
        "--self-contained-html",  # Embed CSS/JS in HTML
        "-s",  # Don't capture output (shows print statements)
        "--durations=10",  # Show slowest 10 tests
    ]

    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    print("🚀 Starting Product Groups Page Tests...")
    print(f"📅 Started at: {datetime.now()}")
    print("🔐 Using existing authentication setup")
    print("-" * 60)

    # Run tests
    exit_code = pytest.main(pytest_args)

    print("-" * 60)
    print(f"✅ Completed at: {datetime.now()}")
    print(f"📊 Exit code: {exit_code}")
    print("📁 Report: reports/product_groups_test_report.html")

    return exit_code

def run_smoke_tests():
    """Run only smoke tests"""
    pytest_args = [
        "tests/test_product_groups_page.py",
        "-v", "-s", "-m", "smoke",
        "--html=reports/product_groups_smoke_report.html",
        "--self-contained-html"
    ]

    os.makedirs("reports", exist_ok=True)
    print("🔥 Running Product Groups Smoke Tests...")
    exit_code = pytest.main(pytest_args)
    print(f"✅ Smoke tests completed: {exit_code}")
    return exit_code

def run_security_tests():
    """Run only security tests"""
    pytest_args = [
        "tests/test_product_groups_page.py",
        "-v", "-s", "-m", "security",
        "--html=reports/product_groups_security_report.html",
        "--self-contained-html"
    ]

    os.makedirs("reports", exist_ok=True)
    print("🔒 Running Product Groups Security Tests...")
    exit_code = pytest.main(pytest_args)
    print(f"✅ Security tests completed: {exit_code}")
    return exit_code

def run_regression_tests():
    """Run regression tests"""
    pytest_args = [
        "tests/test_product_groups_page.py",
        "-v", "-s", "-m", "regression",
        "--html=reports/product_groups_regression_report.html",
        "--self-contained-html"
    ]

    os.makedirs("reports", exist_ok=True)
    print("🔄 Running Product Groups Regression Tests...")
    exit_code = pytest.main(pytest_args)
    print(f"✅ Regression tests completed: {exit_code}")
    return exit_code

def print_usage():
    """Print usage instructions"""
    print("""
🧪 Simplified Test Runner for Product Groups Page

Usage: python simplified_test_runner_product_groups.py [OPTIONS]

Commands:
    all         - Run all tests (default)
    smoke       - Run smoke tests only
    security    - Run security tests only  
    regression  - Run regression tests only

Examples:
    python simplified_test_runner_product_groups.py        # All tests
    python simplified_test_runner_product_groups.py smoke  # Quick tests
    python simplified_test_runner_product_groups.py security # Security tests

Features:
    ✅ Uses existing authentication setup
    ✅ Simple navigation - no complex checks
    ✅ Clean HTML reports
    ✅ Fast execution

Reports: ./reports/
Screenshots: ./screenshots/
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
        elif command == "all":
            exit_code = run_product_groups_tests()
        elif command in ["help", "-h", "--help"]:
            print_usage()
            exit_code = 0
        else:
            print(f"❌ Unknown command: {command}")
            print_usage()
            exit_code = 1
    else:
        exit_code = run_product_groups_tests()

    if exit_code == 0:
        print("\n🎉 All tests completed successfully!")
    else:
        print(f"\n❌ Tests completed with {exit_code} failures")

    sys.exit(exit_code)
# test_runner.py
"""
Test runner script for Products page automation tests
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
        "-m", "not slow",  # Skip slow tests (if any)
    ]

    # Create reports directory if it doesn't exist
    os.makedirs("tests/reports", exist_ok=True)

    print("Starting Products Page Automation Tests...")
    print(f"Test execution started at: {datetime.now()}")
    print("-" * 60)

    # Run tests
    exit_code = pytest.main(pytest_args)

    print("-" * 60)
    print(f"Test execution completed at: {datetime.now()}")
    print(f"Exit code: {exit_code}")

    return exit_code

def run_smoke_tests():
    """Run only smoke tests for quick verification"""
    pytest_args = [
        "tests/test_products_page.py",
        "-v",
        "-m", "smoke",
        "--html=reports/smoke_test_report.html",
        "--self-contained-html",
    ]

    os.makedirs("tests/reports", exist_ok=True)

    print("Running Smoke Tests...")
    return pytest.main(pytest_args)

def run_security_tests():
    """Run only security tests"""
    pytest_args = [
        "tests/test_products_page.py",
        "-v",
        "-m", "security",
        "--html=reports/security_test_report.html",
        "--self-contained-html",
    ]

    os.makedirs("tests/reports", exist_ok=True)

    print("Running Security Tests...")
    return pytest.main(pytest_args)

def run_regression_tests():
    """Run regression tests"""
    pytest_args = [
        "tests/test_products_page.py",
        "-v",
        "-m", "regression",
        "--html=reports/regression_test_report.html",
        "--self-contained-html",
    ]

    os.makedirs("tests/reports", exist_ok=True)

    print("Running Regression Tests...")
    return pytest.main(pytest_args)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()

        if test_type == "smoke":
            exit_code = run_smoke_tests()
        elif test_type == "security":
            exit_code = run_security_tests()
        elif test_type == "regression":
            exit_code = run_regression_tests()
        elif test_type == "all":
            exit_code = run_products_tests()
        else:
            print("Usage: python test_runner.py [smoke|security|regression|all]")
            exit_code = 1
    else:
        exit_code = run_products_tests()

    sys.exit(exit_code)


# conftest_products.py
"""
Additional pytest configuration specifically for products page tests
"""

import pytest
from selenium.webdriver.common.by import By
from pages.products_page import ProductsPage

@pytest.fixture(scope="session")
def products_base_url():
    """Products page specific URL"""
    return "http://localhost/#/pages/catalogue/products/products-list"

@pytest.fixture(scope="function")
def products_page(driver):
    """Products page fixture"""
    page = ProductsPage(driver)
    page.navigate_to_products_page()
    yield page

    # Cleanup: Reset any filters/sorts after each test
    try:
        page.refresh_page()
    except:
        pass  # Ignore cleanup errors

@pytest.fixture(scope="function")
def clean_products_page(driver):
    """Products page fixture with guaranteed clean state"""
    page = ProductsPage(driver)
    page.navigate_to_products_page()
    page.clear_all_search_fields()
    yield page

# Test data fixtures
@pytest.fixture
def test_search_data():
    """Test data for search scenarios"""
    return {
        "valid_sku": "cdf",
        "valid_product_name": "sdfds",
        "invalid_text": "NONEXISTENT123",
        "special_chars": "🥶🥶<>+*&^%$#@!",
        "xss_payload": "<script>alert('test')</script>",
        "sql_payload": "'; DROP TABLE products; --",
        "html_payload": "<h1>test</h1>",
        "large_text": "A" * 1000
    }

@pytest.fixture
def security_test_payloads():
    """Security test payloads"""
    return {
        "xss": [
            "<script>alert('test')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "';alert('XSS');//"
        ],
        "sql": [
            "'; DROP TABLE products; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM users --",
            "admin'--",
            "' OR 1=1 --"
        ],
        "html": [
            "<h1>test</h1>",
            "<b>bold</b>",
            "<iframe src='http://evil.com'></iframe>",
            "<div onclick='alert(1)'>click</div>"
        ]
    }


# pytest_markers.py
"""
Custom pytest markers for organizing tests
"""

import pytest

# Register custom markers
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "smoke: marks tests as smoke tests (quick sanity checks)"
    )
    config.addinivalue_line(
        "markers", "security: marks tests as security-focused tests"
    )
    config.addinivalue_line(
        "markers", "ui: marks tests as UI interaction tests"
    )
    config.addinivalue_line(
        "markers", "regression: marks tests as regression tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )


# Usage Examples:
"""
# Run all tests
python test_runner.py all

# Run only smoke tests
python test_runner.py smoke

# Run only security tests  
python test_runner.py security

# Run only regression tests
python test_runner.py regression

# Run with specific browser
pytest tests/test_products_page.py --browser=firefox

# Run with custom URL
pytest tests/test_products_page.py --base-url=http://localhost:8080

# Run in headless mode
pytest tests/test_products_page.py --headless

# Run specific test class
pytest tests/test_products_page.py::TestProductsPageFiltering

# Run specific test method
pytest tests/test_products_page.py::TestProductsPageFiltering::test_special_character_input_sku_field

# Generate detailed HTML report
pytest tests/test_products_page.py --html=reports/detailed_report.html --self-contained-html

# Run tests in parallel (requires pytest-xdist)
pytest tests/test_products_page.py -n 2

# Run with live logging
pytest tests/test_products_page.py --log-cli-level=INFO

# Skip failing tests and continue
pytest tests/test_products_page.py --continue-on-collection-errors
"""
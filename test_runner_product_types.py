#!/usr/bin/env python3
import os
import sys
import pytest
import argparse
from datetime import datetime

def run_product_types_tests(test_class=None, test_method=None, markers=None,
                            headless=True, verbose=False, html_report=True):
    """
    Run Product Types page tests with specified options.

    Args:
        test_class: Specific test class to run (optional)
        test_method: Specific test method to run (optional)
        markers: List of pytest markers to include (e.g. smoke, regression)
        headless: Run tests in headless mode (no browser UI)
        verbose: Enable verbose output
        html_report: Generate HTML report
    """
    # Set up test target
    test_path = "tests/test_product_types_page.py"
    test_target = test_path

    if test_class:
        test_target += f"::{test_class}"
        if test_method:
            test_target += f"::{test_method}"

    # Prepare pytest arguments
    pytest_args = ["-v"] if verbose else []

    # Add any specified markers
    if markers:
        marker_expr = " or ".join(markers)
        pytest_args.extend(["-m", marker_expr])

    # Set up environment variables
    if headless:
        os.environ["HEADLESS"] = "True"
    else:
        os.environ["HEADLESS"] = "False"

    # Set up reporting
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = "test-reports"
    os.makedirs(report_dir, exist_ok=True)

    if html_report:
        report_path = f"{report_dir}/product_types_tests_{timestamp}.html"
        pytest_args.extend(["--html", report_path, "--self-contained-html"])

    # Add the test target to arguments
    pytest_args.append(test_target)

    # Print test session info
    print(f"Running Product Types page tests: {test_target}")
    if markers:
        print(f"Using markers: {markers}")

    # Run the tests
    exit_code = pytest.main(pytest_args)

    # Report results
    if html_report:
        print(f"\nTest report generated: {report_path}")

    return exit_code

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Product Types page tests")
    parser.add_argument("--class", dest="test_class", help="Specific test class to run")
    parser.add_argument("--method", dest="test_method", help="Specific test method to run")
    parser.add_argument("--markers", nargs="+", help="Test markers to run (smoke, regression, security, ui)")
    parser.add_argument("--no-headless", action="store_true", help="Run with browser visible")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--no-html", action="store_false", dest="html_report", help="Disable HTML report")

    args = parser.parse_args()

    exit_code = run_product_types_tests(
        test_class=args.test_class,
        test_method=args.test_method,
        markers=args.markers,
        headless=not args.no_headless,
        verbose=args.verbose,
        html_report=args.html_report
    )

    sys.exit(exit_code)
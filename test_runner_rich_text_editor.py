# test_runner_rich_text_editor.py
"""
Test runner script for Rich Text Editor Component automation tests
Comprehensive testing for the reusable Description component used across multiple pages
"""

import pytest
import sys
import os
from datetime import datetime

def run_rich_text_editor_tests():
    """Run all rich text editor component tests with comprehensive reporting"""

    # Test execution arguments
    pytest_args = [
        "tests/test_rich_text_editor_component.py",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--html=reports/rich_text_editor_test_report.html",  # HTML report
        "--self-contained-html",  # Embed CSS/JS in HTML
        "--capture=no",  # Show print statements
        "-s",  # Don't capture output (shows setup steps)
        "--durations=15",  # Show slowest 15 tests
    ]

    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    print("🚀 Starting Rich Text Editor Component Automation Tests...")
    print(f"📅 Test execution started at: {datetime.now()}")
    print("📝 Testing reusable Description component (Summernote Editor)")
    print("🔐 Tests will include automatic authentication")
    print("-" * 80)

    # Run tests
    exit_code = pytest.main(pytest_args)

    print("-" * 80)
    print(f"✅ Test execution completed at: {datetime.now()}")
    print(f"📊 Exit code: {exit_code}")
    print("📁 Report saved: reports/rich_text_editor_test_report.html")

    return exit_code

def run_smoke_tests():
    """Run only smoke tests for quick verification"""
    pytest_args = [
        "tests/test_rich_text_editor_component.py",
        "-v",
        "-s",
        "-m", "smoke",
        "--html=reports/rich_text_editor_smoke_report.html",
        "--self-contained-html",
        "--tb=short"
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔥 Running Rich Text Editor Smoke Tests...")
    print("⚡ This will test core functionality quickly")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Smoke tests completed with exit code: {exit_code}")
    return exit_code

def run_security_tests():
    """Run only security tests"""
    pytest_args = [
        "tests/test_rich_text_editor_component.py",
        "-v",
        "-s",
        "-m", "security",
        "--html=reports/rich_text_editor_security_report.html",
        "--self-contained-html",
        "--tb=long"  # Longer traceback for security issues
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔒 Running Rich Text Editor Security Tests...")
    print("🛡️  Testing XSS prevention and input sanitization")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Security tests completed with exit code: {exit_code}")
    return exit_code

def run_regression_tests():
    """Run comprehensive regression tests"""
    pytest_args = [
        "tests/test_rich_text_editor_component.py",
        "-v",
        "-s",
        "-m", "regression",
        "--html=reports/rich_text_editor_regression_report.html",
        "--self-contained-html",
        "--tb=short",
        "--durations=20"  # Show more timing info for regression
    ]

    os.makedirs("reports", exist_ok=True)

    print("🔄 Running Rich Text Editor Regression Tests...")
    print("📋 Testing all editor functionality comprehensively")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Regression tests completed with exit code: {exit_code}")
    return exit_code

def run_performance_tests():
    """Run performance-focused tests"""
    pytest_args = [
        "tests/test_rich_text_editor_component.py::TestRichTextEditorPerformance",
        "-v",
        "-s",
        "--html=reports/rich_text_editor_performance_report.html",
        "--self-contained-html",
        "--tb=short"
    ]

    os.makedirs("reports", exist_ok=True)

    print("⚡ Running Rich Text Editor Performance Tests...")
    print("🚀 Testing editor speed and efficiency")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Performance tests completed with exit code: {exit_code}")
    return exit_code

def run_validation_tests():
    """Run validation-specific tests"""
    pytest_args = [
        "tests/test_rich_text_editor_component.py::TestRichTextEditorValidation",
        "-v",
        "-s",
        "--html=reports/rich_text_editor_validation_report.html",
        "--self-contained-html",
        "--tb=short"
    ]

    os.makedirs("reports", exist_ok=True)

    print("✅ Running Rich Text Editor Validation Tests...")
    print("🔍 Testing input validation and field constraints")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Validation tests completed with exit code: {exit_code}")
    return exit_code

def run_code_view_tests():
    """Run code view specific tests"""
    pytest_args = [
        "tests/test_rich_text_editor_component.py",
        "-v",
        "-s",
        "-k", "code_view",
        "--html=reports/rich_text_editor_code_view_report.html",
        "--self-contained-html",
        "--tb=short"
    ]

    os.makedirs("reports", exist_ok=True)

    print("💻 Running Rich Text Editor Code View Tests...")
    print("🔧 Testing WYSIWYG ↔ Code view functionality")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Code view tests completed with exit code: {exit_code}")
    return exit_code

def run_formatting_tests():
    """Run formatting-specific tests"""
    pytest_args = [
        "tests/test_rich_text_editor_component.py",
        "-v",
        "-s",
        "-k", "font or style or format or color or align",
        "--html=reports/rich_text_editor_formatting_report.html",
        "--self-contained-html",
        "--tb=short"
    ]

    os.makedirs("reports", exist_ok=True)

    print("🎨 Running Rich Text Editor Formatting Tests...")
    print("✨ Testing text styling and formatting features")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Formatting tests completed with exit code: {exit_code}")
    return exit_code

def run_media_tests():
    """Run media insertion tests (links, images, videos)"""
    pytest_args = [
        "tests/test_rich_text_editor_component.py",
        "-v",
        "-s",
        "-k", "link or video or image or table",
        "--html=reports/rich_text_editor_media_report.html",
        "--self-contained-html",
        "--tb=short"
    ]

    os.makedirs("reports", exist_ok=True)

    print("🖼️ Running Rich Text Editor Media Insertion Tests...")
    print("🔗 Testing links, images, videos, and tables")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Media tests completed with exit code: {exit_code}")
    return exit_code

def run_with_browser(browser_name):
    """Run tests with specific browser"""
    pytest_args = [
        "tests/test_rich_text_editor_component.py",
        "-v",
        "-s",
        f"--browser={browser_name}",
        "--html=reports/rich_text_editor_browser_test_report.html",
        "--self-contained-html",
        "-m", "smoke"  # Run smoke tests for browser compatibility
    ]

    os.makedirs("reports", exist_ok=True)

    print(f"🌐 Running Rich Text Editor tests with {browser_name.upper()} browser...")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ {browser_name.upper()} tests completed with exit code: {exit_code}")
    return exit_code

def run_headless_tests():
    """Run tests in headless mode"""
    pytest_args = [
        "tests/test_rich_text_editor_component.py",
        "-v",
        "--headless",
        "--html=reports/rich_text_editor_headless_report.html",
        "--self-contained-html",
        "-m", "smoke"
    ]

    os.makedirs("reports", exist_ok=True)

    print("👻 Running Rich Text Editor tests in HEADLESS mode...")
    print("🖥️  No browser window will be displayed")
    print("-" * 50)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Headless tests completed with exit code: {exit_code}")
    return exit_code

def run_slow_tests():
    """Run slow/comprehensive tests"""
    pytest_args = [
        "tests/test_rich_text_editor_component.py",
        "-v",
        "-s",
        "-m", "slow",
        "--html=reports/rich_text_editor_slow_report.html",
        "--self-contained-html",
        "--tb=short"
    ]

    os.makedirs("reports", exist_ok=True)

    print("🐌 Running Rich Text Editor Slow/Comprehensive Tests...")
    print("🕐 These tests may take longer to complete")
    print("-" * 60)

    exit_code = pytest.main(pytest_args)

    print(f"✅ Slow tests completed with exit code: {exit_code}")
    return exit_code

def print_usage():
    """Print usage instructions"""
    print("""
📝 Rich Text Editor Component Test Runner

Usage: python test_runner_rich_text_editor.py [OPTIONS]

Available Commands:
    all          - Run all rich text editor tests (default)
    smoke        - Run smoke tests (quick verification)
    security     - Run security tests (XSS prevention, sanitization)
    regression   - Run comprehensive regression tests
    performance  - Run performance-focused tests
    validation   - Run input validation tests
    code-view    - Run code view functionality tests
    formatting   - Run text formatting tests
    media        - Run media insertion tests (links, images, videos)
    chrome       - Run smoke tests with Chrome browser
    firefox      - Run smoke tests with Firefox browser
    edge         - Run smoke tests with Edge browser
    headless     - Run smoke tests in headless mode
    slow         - Run slow/comprehensive tests

Examples:
    python test_runner_rich_text_editor.py                # Run all tests
    python test_runner_rich_text_editor.py smoke          # Quick smoke tests
    python test_runner_rich_text_editor.py security       # Security-focused tests
    python test_runner_rich_text_editor.py formatting     # Text formatting tests
    python test_runner_rich_text_editor.py media          # Media insertion tests
    python test_runner_rich_text_editor.py chrome         # Test with Chrome
    python test_runner_rich_text_editor.py headless       # Test without GUI

Component Features Tested:
    📝 WYSIWYG Rich Text Editing
    💻 Code View Toggle (HTML source editing)
    ↩️  Undo/Redo Functionality
    🎨 Text Formatting (Bold, Italic, Underline, Strikethrough)
    🔤 Font Family & Size Selection
    🌈 Text & Background Color
    📐 Text Alignment (Left, Center, Right, Justify)
    📏 Line Height Control
    📋 Lists (Ordered & Unordered)
    🎯 Text Styles (Headers, Paragraphs, Quotes, Code)
    🔗 Link Insertion & Management
    🖼️ Image Upload & URL Insertion
    📹 Video Embedding (YouTube, etc.)
    📊 Table Creation & Management
    ⬆️⬇️ Superscript & Subscript
    📐 Horizontal Rules
    🔧 Toolbar Customization
    ⌨️  Keyboard Shortcuts
    🛡️  XSS Prevention & Input Sanitization
    📱 Responsive Design
    ♿ Accessibility Features

Test Categories:
    🔥 smoke      - Core functionality verification
    🔒 security   - XSS prevention and input sanitization  
    🔄 regression - Comprehensive feature testing
    ⚡ performance - Speed and efficiency testing
    ✅ validation  - Input validation and constraints
    🐌 slow       - Long-running comprehensive tests

Component Usage:
    📍 URL: http://localhost/#/pages/catalogue/products/create-product
    📦 Component: Description (English) - Summernote Editor
    🔄 Reusable: Used across multiple product/content creation pages
    🎯 Purpose: Rich text content creation and editing

Test Scenarios Covered:
    ✅ All 38+ test scenarios from the original specification
    ✅ Code view toggle functionality (Cases 1-3)
    ✅ Undo/Redo operations (Cases 4-5)
    ✅ Font formatting buttons (Cases 6-9)
    ✅ Superscript/Subscript (Cases 10-11)
    ✅ Font family selection (Cases 12-13)
    ✅ Color selection (Cases 14-15)
    ✅ Font size selection (Case 16)
    ✅ Style selection (Cases 17-18)
    ✅ List creation (Case 19)
    ✅ Text alignment (Cases 20-21)
    ✅ Line height (Case 22)
    ✅ Table insertion (Case 23)
    ✅ Link management (Cases 24-33)
    ✅ Video embedding (Cases 34-37)
    ✅ Image insertion (Case 38)
    ✅ Security testing (XSS prevention)
    ✅ Performance testing (large content)
    ✅ Special characters handling
    ✅ Accessibility compliance

Reports Location: ./reports/
Screenshots Location: ./screenshots/

Quality Assurance:
    🔍 Black-box testing approach
    🧪 Component isolation testing
    🚀 Cross-browser compatibility
    📸 Visual regression testing
    🔐 Security vulnerability testing
    ⚡ Performance benchmarking
    ♿ Accessibility compliance testing
    """)

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)

    if len(sys.argv) > 1:
        command = sys.argv[1].lower().replace("-", "_")

        if command == "smoke":
            exit_code = run_smoke_tests()
        elif command == "security":
            exit_code = run_security_tests()
        elif command == "regression":
            exit_code = run_regression_tests()
        elif command == "performance":
            exit_code = run_performance_tests()
        elif command == "validation":
            exit_code = run_validation_tests()
        elif command == "code_view":
            exit_code = run_code_view_tests()
        elif command == "formatting":
            exit_code = run_formatting_tests()
        elif command == "media":
            exit_code = run_media_tests()
        elif command == "chrome":
            exit_code = run_with_browser("chrome")
        elif command == "firefox":
            exit_code = run_with_browser("firefox")
        elif command == "edge":
            exit_code = run_with_browser("edge")
        elif command == "headless":
            exit_code = run_headless_tests()
        elif command == "slow":
            exit_code = run_slow_tests()
        elif command == "all":
            exit_code = run_rich_text_editor_tests()
        elif command in ["help", "h", "_help"]:
            print_usage()
            exit_code = 0
        else:
            print(f"❌ Unknown command: {command}")
            print_usage()
            exit_code = 1
    else:
        exit_code = run_rich_text_editor_tests()

    if exit_code == 0:
        print("\n🎉 All Rich Text Editor tests completed successfully!")
        print("📝 Reusable Description Component is working properly!")
    else:
        print(f"\n❌ Tests completed with {exit_code} failures")
        print("🔍 Check the HTML report for detailed results")

    sys.exit(exit_code)
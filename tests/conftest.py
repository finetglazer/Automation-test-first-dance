import pytest
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_factory import DriverFactory
from config.config import Config

@pytest.fixture(scope="session")
def browser():
    """Browser name fixture"""
    return Config.BROWSER

@pytest.fixture(scope="session")
def base_url():
    """Base URL fixture"""
    return Config.BASE_URL

@pytest.fixture(scope="function")
def driver(browser):
    """WebDriver fixture - creates and quits driver for each test"""
    driver_instance = DriverFactory.get_driver(browser, Config.HEADLESS)
    driver_instance.implicitly_wait(Config.IMPLICIT_WAIT)
    driver_instance.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

    yield driver_instance

    # Cleanup
    driver_instance.quit()

@pytest.fixture(scope="function")
def driver_with_base_url(driver, base_url):
    """WebDriver fixture that navigates to base URL"""
    driver.get(base_url)
    yield driver

def pytest_configure(config):
    """Configure pytest"""
    # Create directories if they don't exist
    for directory in [Config.SCREENSHOTS_DIR, Config.REPORTS_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure"""
    if call.when == "call":
        if call.excinfo is not None and "driver" in item.fixturenames:
            # Get the driver from the test
            try:
                driver = item.funcargs["driver"]
                screenshot_name = f"failure_{item.name}"
                screenshot_path = f"{Config.SCREENSHOTS_DIR}/{screenshot_name}.png"
                driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"Could not take screenshot: {e}")

# Command line options
def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=Config.BASE_URL,
        help="Base URL for testing"
    )
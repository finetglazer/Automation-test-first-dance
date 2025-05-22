import pytest
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_factory import DriverFactory
from config.config import Config
from pages.login_page import LoginPage
from pages.home_page import HomePage

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
def authenticated_driver(driver, base_url):
    """WebDriver fixture that performs login and language setup"""
    try:
        print("\n" + "="*60)
        print("SETTING UP AUTHENTICATED SESSION")
        print("="*60)

        # Step 1: Navigate to login page
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page(base_url)

        # Verify login page loaded
        if not login_page.is_login_page_loaded():
            raise Exception("Login page did not load properly")

        print("✓ Login page loaded successfully")

        # Step 2: Perform login
        login_success = login_page.perform_login(
            username="admin@shopizer.com",
            password="password"
        )

        if not login_success:
            login_page.take_login_screenshot("login_failed")
            raise Exception("Login failed")

        print("✓ Login completed successfully")

        # Step 3: Handle home page and language change
        home_page = HomePage(driver)
        home_page.wait_for_home_page_load()

        if not home_page.is_home_page_loaded():
            raise Exception("Home page did not load after login")

        print("✓ Home page loaded successfully")

        # Step 4: Change language to English if currently French
        current_language = home_page.get_current_language()
        print(f"Current language: {current_language}")

        if home_page.is_french_language():
            print("Changing language from French to English...")

            if home_page.change_language_to_english():
                home_page.wait_for_language_change()
                print("✓ Language changed to English successfully")
            else:
                print("⚠ Could not change language, continuing with current language")
        else:
            print("✓ Language is already English or acceptable")

        print("="*60)
        print("AUTHENTICATION SETUP COMPLETED")
        print("="*60)

        yield driver

    except Exception as e:
        print(f"\n❌ Authentication setup failed: {str(e)}")
        # Take screenshot for debugging
        try:
            driver.save_screenshot("screenshots/auth_setup_failed.png")
            print("Screenshot saved: screenshots/auth_setup_failed.png")
        except:
            pass
        raise

@pytest.fixture(scope="function")
def driver_with_base_url(authenticated_driver, base_url):
    """WebDriver fixture that navigates to base URL (deprecated, use authenticated_driver)"""
    return authenticated_driver

@pytest.fixture(scope="function")
def products_page_ready(authenticated_driver):
    """WebDriver fixture with full setup including navigation to products page"""
    from pages.home_page import HomePage

    try:
        home_page = HomePage(authenticated_driver)

        # Navigate to products page
        if home_page.navigate_to_products_page():
            print("✓ Successfully navigated to products page")
        else:
            print("⚠ Could not navigate via menu, trying direct URL")
            authenticated_driver.get("http://localhost/#/pages/catalogue/products/products-list")

        # Wait for products page to load
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By

        wait = WebDriverWait(authenticated_driver, 15)
        wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Sku']")),
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Product name']"))
            )
        )

        print("✓ Products page loaded and ready for testing")
        return authenticated_driver

    except Exception as e:
        print(f"❌ Failed to setup products page: {str(e)}")
        raise

# Login credentials fixture
@pytest.fixture(scope="session")
def login_credentials():
    """Login credentials fixture"""
    return {
        "username": "admin@shopizer.com",
        "password": "password"
    }

# Page object fixtures
@pytest.fixture(scope="function")
def login_page(driver):
    """Login page fixture"""
    return LoginPage(driver)

@pytest.fixture(scope="function")
def home_page(authenticated_driver):
    """Home page fixture with authenticated driver"""
    return HomePage(authenticated_driver)

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
                # Try to get authenticated_driver first, then driver
                test_driver = None
                if "authenticated_driver" in item.fixturenames:
                    test_driver = item.funcargs.get("authenticated_driver")
                elif "driver" in item.fixturenames:
                    test_driver = item.funcargs.get("driver")

                if test_driver:
                    screenshot_name = f"failure_{item.name}"
                    screenshot_path = f"{Config.SCREENSHOTS_DIR}/{screenshot_name}.png"
                    test_driver.save_screenshot(screenshot_path)
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
    parser.addoption(
        "--skip-auth",
        action="store_true",
        default=False,
        help="Skip authentication setup (for tests that don't need login)"
    )

# Test environment setup helpers
def setup_test_environment():
    """Setup test environment"""
    # Create necessary directories
    directories = [
        Config.SCREENSHOTS_DIR,
        Config.REPORTS_DIR,
        "screenshots/failures",
        "screenshots/debug"
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

# Run setup when conftest is loaded
setup_test_environment()
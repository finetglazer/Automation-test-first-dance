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
    """Optimized WebDriver fixture - faster startup"""
    driver_instance = DriverFactory.get_driver(browser, Config.HEADLESS)
    driver_instance.implicitly_wait(5)  # Reduced from 10 to 5
    driver_instance.set_page_load_timeout(15)  # Reduced from 30 to 15

    yield driver_instance

    # Cleanup
    driver_instance.quit()

@pytest.fixture(scope="function")
def authenticated_driver(driver, base_url):
    """OPTIMIZED WebDriver fixture with faster authentication"""
    try:
        print("\n" + "="*50)
        print("🚀 FAST AUTHENTICATION SETUP")
        print("="*50)

        # OPTIMIZED STEP 1: Quick login
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page(base_url)

        if not login_page.is_login_page_loaded():
            raise Exception("Login page did not load")

        print("✓ Login page ready")

        # STREAMLINED LOGIN
        login_success = login_page.perform_login(
            username="admin@shopizer.com",
            password="password"
        )

        if not login_success:
            raise Exception("Login failed")

        print("✓ Login successful")

        # OPTIMIZED STEP 2: Fast home page handling
        home_page = HomePage(driver)
        home_page.wait_for_home_page_load()

        print("✓ Home page ready")

        # OPTIMIZED STEP 3: Fast language change (if needed)
        if home_page.is_french_language():
            print("🌐 Changing to English...")

            if home_page.change_language_to_english():
                home_page.wait_for_language_change()
                print("✓ Language: English")
            else:
                print("⚠ Language change skipped")
        else:
            print("✓ Language: Already English")

        print("="*50)
        print("✅ FAST SETUP COMPLETED")
        print("="*50)

        yield driver

    except Exception as e:
        print(f"\n❌ Fast authentication failed: {str(e)}")
        # Quick screenshot only on failure
        try:
            driver.save_screenshot("screenshots/fast_auth_failed.png")
        except:
            pass
        raise

@pytest.fixture(scope="function")
def driver_with_base_url(authenticated_driver, base_url):
    """Legacy compatibility fixture"""
    return authenticated_driver

@pytest.fixture(scope="function")
def products_page_ready(authenticated_driver):
    """OPTIMIZED products page setup"""
    from pages.home_page import HomePage

    try:
        home_page = HomePage(authenticated_driver)

        print("🛍️ Quick products page setup...")

        # Fast direct navigation (based on your successful test)
        authenticated_driver.get("http://localhost/#/pages/catalogue/products/products-list")

        # Quick verification with shorter timeout - FIXED: 5 seconds as requested
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By

        try:
            wait = WebDriverWait(authenticated_driver, 5)  # FIXED: Reduced to 5 seconds
            wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Sku']")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Product name']"))
                )
            )
            print("✓ Products page ready")
        except:
            print("⚠ Products page verification timeout (5s), continuing...")

        return authenticated_driver

    except Exception as e:
        print(f"❌ Products page setup failed: {str(e)}")
        raise

# OPTIMIZED login credentials fixture
@pytest.fixture(scope="session")
def login_credentials():
    """Login credentials fixture"""
    return {
        "username": "admin@shopizer.com",
        "password": "password"
    }

# OPTIMIZED page object fixtures
@pytest.fixture(scope="function")
def login_page(driver):
    """Login page fixture"""
    return LoginPage(driver)

@pytest.fixture(scope="function")
def home_page(authenticated_driver):
    """Home page fixture with authenticated driver"""
    return HomePage(authenticated_driver)

def pytest_configure(config):
    """Configure pytest with optimizations"""
    # Create directories if they don't exist
    for directory in [Config.SCREENSHOTS_DIR, Config.REPORTS_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

def pytest_runtest_makereport(item, call):
    """OPTIMIZED screenshot capture - only on failure"""
    if call.when == "call" and call.excinfo is not None:
        # Only take screenshots on test failures to save time
        if "driver" in item.fixturenames:
            try:
                test_driver = None
                if "authenticated_driver" in item.fixturenames:
                    test_driver = item.funcargs.get("authenticated_driver")
                elif "driver" in item.fixturenames:
                    test_driver = item.funcargs.get("driver")

                if test_driver:
                    screenshot_name = f"failure_{item.name}"
                    screenshot_path = f"{Config.SCREENSHOTS_DIR}/{screenshot_name}.png"
                    test_driver.save_screenshot(screenshot_path)
                    print(f"📸 Failure screenshot: {screenshot_path}")
            except Exception as e:
                print(f"Screenshot failed: {e}")

# OPTIMIZED command line options
def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run in headless mode for speed"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=Config.BASE_URL,
        help="Base URL for testing"
    )
    parser.addoption(
        "--fast",
        action="store_true",
        default=False,
        help="Enable fastest possible execution"
    )

# OPTIMIZED test environment setup
def setup_test_environment():
    """Quick test environment setup"""
    directories = [
        Config.SCREENSHOTS_DIR,
        Config.REPORTS_DIR
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)



# Add this fixture to your existing conftest.py file

@pytest.fixture(scope="function")
def product_groups_page_ready(authenticated_driver):
    """OPTIMIZED product groups page setup"""
    from pages.home_page import HomePage

    try:
        home_page = HomePage(authenticated_driver)

        print("🏷️ Quick product groups page setup...")

        # Fast direct navigation to product groups page
        authenticated_driver.get("http://localhost/#/pages/catalogue/products-groups/groups-list")

        # Quick verification with shorter timeout
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By

        try:
            wait = WebDriverWait(authenticated_driver, 5)  # 5 seconds timeout
            wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Code']")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.createBtn"))
                )
            )
            print("✓ Product groups page ready")
        except:
            print("⚠ Product groups page verification timeout (5s), continuing...")

        return authenticated_driver

    except Exception as e:
        print(f"❌ Product groups page setup failed: {str(e)}")
        raise


# Run setup when conftest is loaded
setup_test_environment()

